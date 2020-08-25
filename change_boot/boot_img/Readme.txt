4. WinSCP 같은 SFTP 프로그램을 이용하여 eon에 splash.img 파일을 업로드 합니다.
  ( 업로드 위치는 /sdcard/splash.img 입니다. /storage/emulated/0/splash.img 도 결국 같은 위치입니다. )
5. eon에 ssh 연결하여 아래 명령어를 입력합니다.
Code:
su
dd if=/sdcard/splash.img of=/dev/block/bootdevice/by-name/splash
6. 재시작 하면 다음부터 바뀐 로고로 부팅됩니다.
