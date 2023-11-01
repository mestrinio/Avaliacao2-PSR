<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<div align="center">

[![Contributors][contributors-shield]][contributors-url]




<!-- PROJECT LOGO -->
<br />

  <a href="https://github.com/mestrinio/Avaliacao2-PSR/graphs/">
    <img src="docs/LOGO.png" alt="Logo" width="550" height="350">
  </a>

<h3 align="center">PSR - Trabalho Prático 2</h3>

<h2><b> Repository Owner: Pedro Martins 103800
<br>Collaborators: Gustavo Reggio & Tomás Taxa </b></h2>

  <p align="center">
    This repository was created for evaluation @ Robotic Systems Programming "PSR 23-24 Trabalho prático 2".
    <br />
    <!-- <a href="https://github.com/mestrinio/Avaliacao2-PSR"><strong>Explore the Wiki »</strong></a> -->
    <br >
    <a href="https://github.com/mestrinio/Avaliacao2-PSR/issues"> <u>Make Suggestion</u> </a>
  </p>
</div>
<br>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-assignment">About the assignment</a>
    </li>
     <li>
      <a href="#Objectives">Objectives</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#Setup">Setup</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>
<br>



<!-- ABOUT THE ASSIGNMENT -->
## About the Assignment
<div align="center">
<img  src="docs/tracking.gif" alt="GIF animated" width="400">
</div>
<br>

This assignment was developed for Robotic Systems Programming. It is an Augmented Reality Painting program, which uses the computer webcam to detect a specific chosen color, and with that, draw on the exact position in a white canvas. This uses Python's OpenCV and includes some advanced features requested by the teacher.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ### Built With

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- Objectives -->
## Objectives
### Color Segmenter
The color segmenter program asks the user what parameters for color detection he wants. This part captures the webcam and shows 6 trackbars on the image so that the user can define the right color detection for whatever object he wants to use for painting. Then saves these values on a JSON file.

<h1> INSERT IMAGE HERE *************</h1>

### AR Paint

The actual painting part of the program should accomplish the following requirements:

#### SETUP
- Read the arguments on the command line to path the json file;
- Read the json file specified in the path, that has the color limits;
- Setup the webcam's capture;
- Create a white canvas to draw on, which has the same size as the incoming capture video of the webcam;

#### CONTINUOUS
- Record and show each webcam's frame;
- Process the incoming video feed with a mask containing the desired pixel color values (and show the mask on another window);
- Process the mask to obtain only the biggest object, and show it;
- Calculate that object's centroid (and mark it as a red cross 'X' on the webcam's feed);
- Use that centroid to paint a circle or a line in the white canvas, with the chosen characteristics for the painting;
***
##### Keybindings:
- 'R' to change brush color to <p style="color: rgb(255,0,0)">RED</p>
- 'G' to change brush color to <p style="color: rgb(0,255,0)">GREEN</p>
- 'B' to change brush color to <p style="color: rgb(0,0,255)">BLUE</p>
- '+' to increase brush size
- '-' to decrease brush size
- 'C' to clear the canvas
- 'W' to save the current canvas to an image file
- 'Q' shutdown the program

***
#### Advanced features
##### Use Shake Protection
The program is designed to draw lines between centroids instead of circles in each centroid


<!-- GETTING STARTED -->
## Getting Started

This is a Python file, so it should be ran in a dedicated terminal running main.py, which is the file that runs the entire program, it can be found under /src directory.

```
./main.py
```



## Setup
<h3><b>Libraries</b></h3>

To run the program, the following libraries should be installed:
```
sudo apt install python3 python3-tk
sudo apt install python3-pip
pip install pygame
pip install gtts
pip install opencv-python
pip install imutils
pip install numpy
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### How it works


Run main.py:
- Show your beautiful face to the camera;



- When prompted to, write your name and press save or hit Enter, it shall now detect your face, identify it, and track it even when you get obstructed by something or leave the camera FOV and come out on the opposite side;

<br>
<br>
<div align="center">
<img  src="docs/entername.png" alt="entername" height="150"><img  src="docs/savename.png" alt="savename" height="150">
</div>
<div align="center">Prompt to save your name (click save or hit Enter)</div>

<br>
<br>
<div align="center">
<img  src="docs/detected.png" alt="detected" height="200">
</div>
<div align="center">Started recognizing and tracking the face</div>

<br>
<br>
<br>
<br>

<div align="center">
<img  src="docs/dissapearing.png" alt="dissapearing" height="150"><img  src="docs/dissapeared.png" alt="dissapeared" height="150"><img  src="docs/reappearing.png" alt="reappearing" height="150">
</div>

<div align="center">Disappearing from one side and appearing on the other </div>

<br>
<br>
<br>
<br>
<div align="center">
<img  src="docs/detectedobstruct.png" alt="obstructed" height="150">
</div>
<div align="center">Tracking the face even when obstructed</div>
<br>
<br>

- Show other faces and repeat.



<br>

Arguments when running main.py:
- -c (defines which Haar Cascade it is used for detection);
- -t (defines which tracking method is going to be used).





<!-- CONTACT -->
## Contact
Alexandre Carola - amcc@ua.pt


Bruno Silva - bruno.favs@ua.pt


Pedro Martins - pedro.mestre@ua.pt

Project Link: [Trabalho Prático 1](https://github.com/brunofavs/SAVI_TP1)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Professor Miguel Oliveira - mriem@ua.pt

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/RobutlerAlberto/RobutlerAlberto.svg?style=for-the-badge
[contributors-url]: https://github.com/mestrinio/Avaliacao2-PSR/graphs/contributors
[product-screenshot]: docs/logo.png