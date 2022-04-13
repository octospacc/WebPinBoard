#!/usr/bin/env python3
LICENSE = """
<!--
    WebPinBoard
    Copyright (C) 2022, OctoSpacc
    https://gitlab.com/octospacc

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
"""

BaseHTML = """
<!DOCTYPE html>
{LICENSE}
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>{TITLE}</title>
	<link rel="stylesheet" href="https://unpkg.com/98.css">
	<link rel="stylesheet" href="Style.css">
</head>
<body>
	<div id="Background"> <!-- https://pixelfed.uno/i/web/post/419157143827461664 (CC BY-SA 4.0) -->
		<img src="https://i.imgur.com/GwCgSFC.png"> <!-- https://i.imgur.com/5bdkMlg.gif -->
	</div>
	<div class="BoardsContainer">
		{INFO}
		{BOARDS}
	</div>
</body>
</html>
"""

InfoHTML = """
<div class="InfoWindow">
	<label for="{TITLE}-Toggle"><p>Info Open/Close</p></label>
	<input type="checkbox" id="{TITLE}-Toggle" {CHECKBOX}>
	<div class="InfoWindowBody">
		<{H}>{TITLE}</{H}>
		{CONTENT}
	</div>
</div>
"""

BoardHTML = """
<div class="window">
	<div class="title-bar">
		<div class="title-bar-text">
			{TITLE}
		</div>
		<div class="title-bar-controls">
			<label for="{TITLE}-Toggle"><pre></pre></label>
		</div>
	</div>
	<input type="checkbox" id="{TITLE}-Toggle" {CHECKBOX}>
	<div class="window-body">
		{CONTENT}
	</div>
</div>
"""

from markdown import Markdown

def SplitPop(String, Key):
	List = String.split(Key)
	for i,s in enumerate(List):
		if not s:
			List.pop(i)
	return List

def GetHeading(HTML):
	return 'h' + HTML.split('<h')[1].split('>')[0]

def GetDataHTML():
	Path = 'Data.md'
	try:
		with open(Path, 'r') as f:
			return Markdown().convert(f.read()).replace('\n','')
	except Exception:
		print("Can't load {} file for reading. Exiting.".format(Path))
		exit(1)

def GetBoards(Data):
	Boards = SplitPop(Data, '<h')
	for i,b in enumerate(Boards):
		Boards[i] = '<h' +b
	return Boards

def GetBoardParams(Title):
	if Title.endswith(':Closed'):
		Checkbox = 'checked'
		Title = Title[:-len(':Closed')-1]
	else:
		Checkbox = ''
	return (Title, Checkbox)

def GenBoard(Data, Template):
	Heading = GetHeading(Data)

	Elements = SplitPop(
		SplitPop(
			Data,
			'<{}>'.format(Heading))[0],
		'</{}>'.format(Heading))

	Title, Checkbox = GetBoardParams(Elements[0])

	Board = Template.format(
		H=Heading,
		TITLE=Title,
		CHECKBOX=Checkbox,
		CONTENT=Elements[1]
	)

	return Board

def WriteHTML(Info, Boards):
	Path = 'index.html'

	InfoBoard = GenBoard(Info, InfoHTML)
	HTMLBoards = ''
	for b in Boards:
		HTMLBoards += GenBoard(b, BoardHTML)

	Heading = GetHeading(Info)
	Title = SplitPop(
		SplitPop(
			Info,
			'<{}>'.format(Heading))[0],
		'</{}>'.format(Heading))[0]

	Title, Checkbox = GetBoardParams(Title)

	try:
		with open(Path, 'w') as f:
			f.write(
				BaseHTML.format(
					LICENSE=LICENSE,
					TITLE=Title,
					CHECKBOX=Checkbox,
					INFO=InfoBoard,
					BOARDS=HTMLBoards))
		return True
	except Exception:
		raise
		print("Can't load {} file for writing. Exiting.".format(Path))
		exit(1)

def Main():
	Boards = GetBoards(
		GetDataHTML().replace(
			'<img', '<img loading="lazy"'))
	Info = Boards[0]
	Boards.pop(0)
	WriteHTML(Info, Boards)

if __name__ == '__main__':
	Main()
