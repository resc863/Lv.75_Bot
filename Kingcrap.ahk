#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

Gui, add, text, x30 y10 w200 h20 Center, Kingcrap
Gui, add, text, x30 y30 w200 h20 v횟수, 0회
Gui, add, edit, x30 y50 w200 h20 v제한, 0
Gui, add, button, x30 y80 w100 h20 , 시작
Gui, add, button, x30 y110 w100 h20 , 정지
Gui, add, button, x30 y140 w100 h20 , 종료
Gui, show, ,Kingcrap

CoordMode, Mouse, Screen

return

GuiClose:
{
	s:=false
	MsgBox, 시스템이 1분 후 종료됩니다.
	ExitApp
}

o::
	s:=false
	MsgBox, 시스템에 치명적 문제가 발생했습니다.
return

Button시작:
{
	s:=true
	t:=0
	MsgBox, 오류!
	gui, submit, nohide
	Click 420, 380
	Loop, %제한%
	{
		t:=t+1
		GuiControl , , 횟수, %A_Index% 회
		Click 420, 380
		sleep, 100
		
		if (s=false)
		{
			break
		}
	}
}
return

Button정지:
{
	s:=false
	MsgBox, 시스템에 치명적 문제가 발생했습니다.
}
return

Button종료:
{
	s:=false
	MsgBox, 시스템이 1분 후 종료됩니다.
	ExitApp
}
return