# Prompt — Montagem sincronizada em colagem de papel

Vou enviar, nesta ordem: (1) clipes de vídeo em estilo colagem de papel, (2) o áudio da narração, (3) uma trilha sonora. Edite um vídeo final sincronizado seguindo estas regras.

## 1. Análise antes de editar (não renderize nada ainda)

1. Use `ffprobe` em todos os clipes e informe duração, resolução e fps de cada um. Some a duração total e compare com a duração da narração.
2. Extraia 3 quadros de cada clipe, monte uma folha de contato e descreva o que aparece em cada um.
3. Verifique o texto visível nos clipes: palavras em outro idioma, palavras sem sentido, documentos falsos, números sem contexto. Liste os problemas com clipe e tempo.
4. Transcreva a narração com marcação de tempo (ElevenLabs Scribe) e detecte as pausas com `silencedetect` (-35 dB, 0,15 s). Divida a narração em frases com início e fim.

## 2. Plano de corte (mostre como tabela e espere minha aprovação)

- Associe cada frase ao clipe que a ilustra **pelo conteúdo, não pela ordem de envio**. Se a narração for cronológica, reordene os clipes.
- Cada corte cai no início de uma frase, em uma pausa da narração.
- Limites de tempo por clipe:
  - desacelerar até **0,67x** no máximo; abaixo disso, congelar o último quadro;
  - acelerar até **1,33x** no máximo;
  - se o trecho for mais curto que o clipe, usar o trecho do clipe que mostra o elemento-chave, normalmente o final, onde a animação já montou a cena.
- Avise qualquer trecho que precise de **mais de 3 s de quadro congelado** ou que caiba em **menos de 2,5 s**. Nesses casos, diga que clipe novo eu deveria gerar.
- Mostre a tabela:

| Tempo | Trecho da narração | Clipe | Velocidade | Congelamento |
|---|---|---|---|---|

## 3. Montagem (depois da aprovação)

- `ffmpeg`, mantendo a resolução e o fps originais (não aumentar a resolução).
- Ao mudar a velocidade, duplicar quadros sem interpolação: combina com a estética stop-motion de papel.
- **Abertura:** 1,5 s com o primeiro quadro parado e fade-in. Narração começa em 1,5 s.
- **Final:** cerca de 3,5 s depois da última palavra, com o último clipe em câmera lenta e fade-out de vídeo e áudio.

## 4. Áudio

- Medir o volume (LUFS) da narração e da trilha com `ebur128`.
- Baixar a trilha até ficar cerca de **10 a 12 dB abaixo da voz**.
- Abaixar a música automaticamente quando houver voz (`sidechaincompress` com a narração como chave: threshold 0.02, ratio 8, attack 40 ms, release 600 ms).
- Se a trilha começar muito baixa, começar a partir do ponto em que ela já tem corpo.
- Fade-out da música nos últimos 2,5 s.
- Normalizar a mixagem final para **-14 LUFS** com pico de **-1,5 dBTP**.
- **Saída:** MP4 H.264 + AAC 192 kbps, 48 kHz, com `+faststart`.

## 5. Entrega

- Envie o MP4 e um relatório curto com o mapa de corte final e os pontos fracos que ficaram: trechos esticados, erros de texto não corrigidos, dúvidas de licença da trilha.
- Salve o script de montagem em Python junto com o vídeo, para eu poder refazer com ajustes.
- Não esconda problemas: se algo não ficou bom, diga.
