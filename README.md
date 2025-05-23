<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Comentario de varias líneas
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">Pychess</h1>
</div>
<div align="center">
    Play chess at any moment with your friends on any device!
</div>

<!-- ABOUT THE PROJECT -->
## Details
#### 🐍 LANGUAGE: Python  
#### 👤 AUTHORS: [javiiervm](https://github.com/javiiervm) (backend) & [iikerm](https://github.com/iikerm) (frontend)
<br />

## Features

☑️ Compatible with Windows, Linux, Android (tested using Pydroid3), and macOS.

☑️ Touchscreen support.

☑️ Classic chess game mode.

☑️ Castling enabled.

☑️ When a Pawn reaches the end of the board, it turns into Queen automatically.

## Requirements
To be able to run this program properly, you need to have **Python** installed (the Tkinter library is included with the installation). You can download it in your device through [Python's official website](https://www.python.org/). *The program has been tested with Python 3.12*
> [!IMPORTANT]
> If you want to run this program **on Android**, the best way to do so is by installing [Pydroid3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3&pcampaignid=web_share), a Python emulator to write and run Python codes. To make it work, just download the .zip source code, unzip the file (you can use an app like [RAR](https://play.google.com/store/apps/details?id=com.rarlab.rar&pcampaignid=web_share) for that) and then open MainGUI.pyw in the editor and touch the "Run" button.
>
> Other great option is to use [Termux](https://play.google.com/store/apps/details?id=com.termux&pcampaignid=web_share), a terminal for Android, you can install Python there or even install a Linux distro as an isolated environment to run code.

## Workflow
This program allows you to play chess on your PC locally with a friend, with a round system so you move your pieces in turns, following the classic chess workflow.

* When opened, the program displays the board automatically with all the pieces ready, black goes at the top and white goes at the bottom. White starts.  
  <div align="center">
    <img src="https://github.com/user-attachments/assets/ec36abc0-db2d-42a6-ae82-aef098ff08a7" width="50%" />
  </div>

* When clicking or touching a piece, the board will automatically display the squares to which it can be moved. 
  <div align="center">
    <img src="https://github.com/user-attachments/assets/881de647-94ac-4fd2-a2b6-a8f7c7b8099f" width="50%" />
  </div>

* Only movements that can save the king are allowed when it is in danger. This is checked automatically by the program.
  <div align="center">
    <img src="https://github.com/user-attachments/assets/e4bf75ce-f18e-432c-8390-20f689c6bc56" width="50%" />
  </div>

* Game ends automatically when a checkmate happens! 
  <div align="center">
    <img src="https://github.com/user-attachments/assets/b8d9647b-6bcf-4900-81c3-cddd85929962" width="50%" />
  </div>

## Future updates and pending work
* Add support for iOS.
* Movement counter when the king is the last piece alive to allow ties.
* When a Pawn reaches the end of the board, allow the player to choose between Queen, Rook, Bishop and Knight instead of turning it into Queen by default.
* Progress saver to continue the game later.
* Online connection to play with friends that are far away!
* New game modes!
