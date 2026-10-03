import subprocess,glob,os
U='/root/.claude/uploads/1c1f1728-865b-5c04-ac83-e65000ba9a97'; S=os.path.dirname(os.path.abspath(__file__))
ids=['36d17f74','de9b9f8a','ff380cc5','f4845bc1','4963805c','1bf59bdc','48b2232e','34117c63','44bcf9aa','b2bc1b01']
F=[glob.glob(f'{U}/{i}*.mp4')[0] for i in ids]
plan=[(4,0,6.016,7.84),(1,0,6.016,7.45),(8,0.8,6.016,5.20),(5,0.37,6.016,5.63),(9,0,6.016,8.48),
      (3,0,6.016,6.24),(6,0,6.016,12.74),(7,0,6.016,8.19),(10,3.0,6.016,2.26),(2,1.0,6.016,6.50)]
os.makedirs(f'{S}/seg',exist_ok=True); L=open(f'{S}/list.txt','w')
for n,(c,a,b,d) in enumerate(plan,1):
    ln=b-a; r=min(d/ln,1.5); pad=max(d-ln*r,0)+0.5
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',F[c-1],'-vf',
      f'setpts={r:.4f}*PTS,fps=24,tpad=stop_mode=clone:stop_duration={pad:.3f},trim=duration={d},setpts=PTS-STARTPTS,format=yuv420p',
      '-an','-c:v','libx264','-crf','16','-preset','slow',f'{S}/seg/{n}.mp4'],check=True)
    L.write(f"file '{S}/seg/{n}.mp4'\n"); print(f'{n:2} clip{c:<2} {d:5.2f}s velocidade {1/r:.2f}x congela {max(d-ln*r,0):.2f}s')
L.close()
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{S}/list.txt','-c','copy',f'{S}/video.mp4'],check=True)
M=glob.glob(f'{U}/e52a25b7*.mp3')[0]; V=glob.glob(f'{U}/b7ce31a1*.wav')[0]; T=72.0
fc=("[0:v]tpad=start_mode=clone:start_duration=1.5,fade=t=in:d=0.8,fade=t=out:st=70.5:d=1.5[v];"
    "[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay=1500|1500,apad,asplit=2[voz][key];"
    "[2:a]aresample=48000,volume=-14dB[mus];"
    "[mus][key]sidechaincompress=threshold=0.02:ratio=8:attack=40:release=600:makeup=1[duck];"
    "[duck]afade=t=in:d=0.5,afade=t=out:st=69.5:d=2.5[bed];"
    "[voz][bed]amix=inputs=2:normalize=0:duration=first,atrim=0:72,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{S}/video.mp4','-i',V,'-i',M,'-filter_complex',fc,
  '-map','[v]','-map','[a]','-t',str(T),'-c:v','libx264','-crf','18','-preset','slow','-c:a','aac','-b:a','192k',
  '-ar','48000','-movflags','+faststart','/home/user/Lula/lula_montagem.mp4'],check=True)
