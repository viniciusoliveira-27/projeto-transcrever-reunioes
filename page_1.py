from pathlib import Path
from datetime import datetime
import time
import queue

from streamlit_webrtc import WebRtcMode, webrtc_streamer 
import streamlit as st

import pydub
import openai
from dotenv import load_dotenv, find_dotenv

# forma de pegar o caminho completo do arquivo
PASTA_ARQUIVOS = Path(__file__).parent / 'arquivos'
PASTA_ARQUIVOS.mkdir(exist_ok=True)

PROMPT = '''
Faça um resumo do texto delimitado por ####
O texto é a transcrição de uma conversa formal / informal.
O resumo deve contar com os principais assuntos discutidos na conversa.
O resumo deve ter no maximo 1000 caracteres.
O resumo deve estar em texto corrido.
No final, devem ser apresentados os principais pontos discutidos na conversa no formato de bullet points.

o formato final que eu desejo é o seguinte:

Resumo conversa:
 - escrever aqui o resumo.

 principais pontos discutidos:
  - ponto 1
  - ponto 2
  - ponto 3
  - ponto n



texto: ####{}####


'''

_ = load_dotenv(find_dotenv())

def salva_arquivo(caminho_arquivo, conteudo):
    with open(caminho_arquivo, 'w') as f:
        f.write(conteudo)

def le_arquivo(caminho_arquivo):
    if caminho_arquivo.exists():
        with open(caminho_arquivo) as f:
            return f.read()
    else:
        return ''



def listar_reunioes():
    lista_reunioes = PASTA_ARQUIVOS.glob('*')
    lista_reunioes = list(lista_reunioes)
    lista_reunioes.sort(reverse=True)
    reunioes_dict = {}
    for pasta_reuniao in lista_reunioes:
        data_reuniao = pasta_reuniao.stem
        ano, mes, dia, hora, min, seg = data_reuniao.split('-')
        reunioes_dict[data_reuniao] = f'{ano}-{mes}-{dia} {hora}:{min}:{seg}'
        titulo = le_arquivo(pasta_reuniao / 'titulo.txt')
        if titulo != '':
            reunioes_dict[data_reuniao] += f' - {titulo}'
    return reunioes_dict

# OPENAI UTILS =====================
client = openai.OpenAI()

def transcreve_audio(caminho_audio, language='pt', response_format='text'):
    with open(caminho_audio, 'rb') as arquivo_audio:
        transcricao = client.audio.transcriptions.create(
            model='whisper-1',
            language=language,
            response_format=response_format,
            file=arquivo_audio,
        )
    return transcricao

def chat_openai(
        mensagem,
        modelo='gpt-4o-mini-2024-07-18',
    ):
    mensagens = [{'role': 'user', 'content': mensagem}]
    resposta = client.chat.completions.create(
        model=modelo,
        messages=mensagens,
        )
    return resposta.choices[0].message.content

# TAB GRAVA REUNIÃO =====================

def adiciona_chunck_audio(frames_de_audio, audio_chunck):
    for frame in frames_de_audio:
        sound = pydub.AudioSegment(
            data=frame.to_ndarray().tobytes(),
            sample_width=frame.format.bytes,
            frame_rate=frame.sample_rate,
            channels=len(frame.layout.channels)
        )
        audio_chunck += sound
    return audio_chunck

def tab_grava_reuniao():
    webrtx_ctx = webrtc_streamer(
        key='recebe_audio',
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=4096,
        media_stream_constraints={
            'audio': True,
            'video': False,
        },
    )
    if not webrtx_ctx.state.playing:
        return
    
    container = st.empty()
    container.markdown('**Comece a falar**')
    pasta_reuniao = PASTA_ARQUIVOS / datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    pasta_reuniao.mkdir()


    ultima_transcricao = time.time()
    audio_completo = pydub.AudioSegment.empty()
    audio_chunck = pydub.AudioSegment.empty()
    transcricao = ''

    # loop para ir pegando os frames de audio enquanto o start estiver dado
    while True:
        if webrtx_ctx.audio_receiver:
            # container.markdown('**Gravando...**')
            try:
                frames_de_audio = webrtx_ctx.audio_receiver.get_frames(timeout=1)
            except queue.Empty:
                time.sleep(0.1)
                continue
            audio_completo = adiciona_chunck_audio(frames_de_audio, audio_chunck)
            audio_chunck = adiciona_chunck_audio(frames_de_audio, audio_chunck)
            if len(audio_chunck) > 0 and audio_chunck.dBFS > -30:
                audio_completo.export(pasta_reuniao / 'audio.mp3')   
                agora = time.time()
                if agora - ultima_transcricao > 15:
                    ultima_transcricao = agora
                    audio_chunck.export(pasta_reuniao / 'audio_temp.mp3')
                    transcricao_chunck = transcreve_audio(pasta_reuniao / 'audio_temp.mp3')
                    transcricao += transcricao_chunck
                    salva_arquivo(pasta_reuniao / 'transcricao.txt', transcricao)
                    container.markdown(transcricao)

                    audio_chunck = pydub.AudioSegment.empty()              
                
        else:
            break




# TAB SELEÇÃO REUNIÃO =====================
def tab_selecao_reuniao():
     reunioes_dict = listar_reunioes()
     if len(reunioes_dict) > 0:
        reunioao_selecionada = st.selectbox('Selecione uma reunião', 
                                         list(reunioes_dict.values()))
        st.divider()
        reuniao_data = [k for k, v in reunioes_dict.items() if v == reunioao_selecionada][0]
        pasta_reuniao = PASTA_ARQUIVOS / reuniao_data
        if not (pasta_reuniao / 'titulo.txt').exists():
            st.warning('Adicione um titulo para a reunião')
            titulo_reuniao = st.text_input('Título da reunião', key='titulo_input')
            if st.button('Salvar'):
                salvar_titulo(pasta_reuniao, st.session_state.titulo_input)
                st.success('Título salvo com sucesso!')
                st.rerun()

            # st.button('Salvar',
            #           on_click=salvar_titulo,
            #           args=(pasta_reuniao, titulo_reuniao))
        else:
            titulo = le_arquivo(pasta_reuniao / 'titulo.txt')
            transcricao = le_arquivo(pasta_reuniao / 'transcricao.txt')
            resumo = le_arquivo(pasta_reuniao / 'resumo.txt')
            if resumo == '':
                gerar_resumo(pasta_reuniao)
                resumo = le_arquivo(pasta_reuniao / 'resumo.txt')
            
            st.markdown(f' ## {titulo}')            
            st.markdown(f' Transcrição: {transcricao}')
            st.markdown(f' Resumo: {resumo}')

def salvar_titulo(pasta_reuniao, titulo):
    salva_arquivo(pasta_reuniao / 'titulo.txt' , titulo)
   
def gerar_resumo(pasta_reuniao):
    transcricao = le_arquivo(pasta_reuniao / 'transcricao.txt')
    resumo = chat_openai(mensagem = PROMPT.format(transcricao))  
    salva_arquivo(pasta_reuniao / 'resumo.txt', resumo)  

    pass
# MAIN =====================
def main():
    st.header('Bem-vindo ao ChatToNote 🎙️', divider=True)
    tab_gravar, tab_selecao = st.tabs(['Gravar Reunião', 'Ver transcrições salvas'])
    with tab_gravar:
        tab_grava_reuniao()
    with tab_selecao:
        tab_selecao_reuniao()

if __name__ == '__main__':
    main()