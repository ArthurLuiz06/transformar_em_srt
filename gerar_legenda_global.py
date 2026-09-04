import sys
import os
import whisper
import ollama

if len(sys.argv) < 2:
    print("Uso correto: python gerar_legenda_global.py nome_do_video.mp4")
    sys.exit(1)

video_path = sys.argv[1]
if not os.path.exists(video_path):
    print(f"Erro: O arquivo '{video_path}' não foi encontrado.")
    sys.exit(1)

base_name = os.path.splitext(video_path)[0]
srt_output = f"{base_name}.srt"

print(f"Carregando o modelo Whisper local para o vídeo: {video_path}...")
model = whisper.load_model("base")

print("Realizando a transcrição bruta...")
result = model.transcribe(video_path, language="pt")

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

def split_text_into_chunks(text, max_chars=30):
    words = text.split()
    chunks = []
    current_chunk = ""
    for word in words:
        if len(current_chunk + " " + word) <= max_chars:
            current_chunk = (current_chunk + " " + word).strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = word
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

srt_lines = []
subtitle_index = 1
segments = result.get("segments", [])

print("Processando e corrigindo trechos com o Ollama local...")
for segment in segments:
    start_base = segment["start"]
    end_base = segment["end"]
    raw_text = segment["text"].strip()
    
    # Envia o trecho para o Ollama corrigir erros fonéticos (como "matar a efe" -> "matar o tempo")
    try:
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'system',
                'content': 'Corrija erros de reconhecimento de voz, fonéticos e gramaticais deste trecho de legenda em português do Brasil, mantendo exatamente o mesmo sentido informal. Retorne apenas o texto corrigido, sem explicações ou aspas.'
            },
            {
                'role': 'user',
                'content': raw_text
            },
        ])
        corrected_text = response['message']['content'].strip()
    except Exception:
        corrected_text = raw_text  # Fallback se o Ollama falhar

    chunks = split_text_into_chunks(corrected_text, max_chars=28)
    total_chunks = len(chunks)
    
    if total_chunks == 0:
        continue
        
    duration = (end_base - start_base) / total_chunks
    
    for i, chunk in enumerate(chunks):
        chunk_start = start_base + (i * duration)
        chunk_end = start_base + ((i + 1) * duration)
        
        srt_lines.append(f"{subtitle_index}\n{format_time(chunk_start)} --> {format_time(chunk_end)}\n{chunk}\n")
        subtitle_index += 1

with open(srt_output, "w", encoding="utf-8") as f:
    f.write("\n".join(srt_lines))

print(f"Sucesso! Legenda perfeita gerada em: {srt_output}")