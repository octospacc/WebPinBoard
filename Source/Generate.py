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
	<link rel="stylesheet" href="https://unpkg.com/98.css"> <!-- Credits: https://github.com/jdan/98.css -->
	<link rel="stylesheet" href="Style.css">
</head>
<body>
	<div id="Background"> <!-- https://pixelfed.uno/i/web/post/419157143827461664 (CC BY-SA 4.0) -->
		<img src="https://i.imgur.com/GwCgSFC.png"> <!-- https://i.imgur.com/5bdkMlg.gif -->
	</div>
	<div class="InfoWindow">
		<label for="{TITLE}-Toggle"><p>Info Open/Close</p></label>
		<input type="checkbox" id="{TITLE}-Toggle">
		<div class="InfoWindowBody">
			{INFO}
		</div>
	</div>
{BOARDS}
</body>
</html>
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
		<input type="checkbox" id="{TITLE}-Toggle">
		<div class="window-body">
			{CONTENT}
		</div>
	</div>
"""

# TODO: Just make it work with any heading by itself.. smh
MainHeading = 'h3'

from markdown import Markdown

def SplitPop(String, Key):
	List = String.split(Key)
	for i,s in enumerate(List):
		if not s:
			List.pop(i)
	return List

def GetDataHTML():
	Path = 'Data.md'
	try:
		with open(Path, 'r') as f:
			return Markdown().convert(f.read()).replace('\n','')
	except Exception:
		print("Can't load {} file for reading. Exiting.".format(Path))
		exit(1)

def GetBoards(Data):
	Boards = SplitPop(Data, '<{}>'.format(MainHeading))

	for b in range(len(Boards)):
		Boards[b] = '<{}>'.format(MainHeading) + Boards[b]

	return Boards

def GenBoard(Data):
	Elements = SplitPop(
		SplitPop(
			Data,
			'<{}>'.format(MainHeading))[0],
		'</{}>'.format(MainHeading))
	Board = BoardHTML.format(
		TITLE=Elements[0],
		CONTENT=Elements[1]
	)

	return Board

def WriteHTML(Info, Boards):
	Path = 'WebPinBoard.html'

	HTMLBoards = ''
	for b in Boards:
		HTMLBoards += GenBoard(b)

	Title = SplitPop(
		SplitPop(
			Info,
			'<{}>'.format(MainHeading))[0],
		'</{}>'.format(MainHeading))[0]

	try:
		with open(Path, 'w') as f:
			f.write(
				BaseHTML.format(
					LICENSE=LICENSE,
					TITLE=Title,
					INFO=Info,
					BOARDS=HTMLBoards))
		return True
	except Exception:
		raise
		print("Can't load {} file for writing. Exiting.".format(Path))
		exit(1)

def Main():
	Boards = GetBoards(GetDataHTML())
	Info = Boards[0]
	Boards.pop(0)
	WriteHTML(Info, Boards)

if __name__ == '__main__':
	Main()
