<p align="center">
  <img src="https://www.especial.gr/wp-content/uploads/2019/03/panepisthmio-dut-attikhs.png" alt="UNIWA" width="150"/>
</p>

<p align="center">
  <strong>UNIVERSITY OF WEST ATTICA</strong><br>
  SCHOOL OF ENGINEERING<br>
  DEPARTMENT OF COMPUTER ENGINEERING AND INFORMATICS
</p>

<hr/>

<p align="center">
  <strong>Information Retrieval</strong>
</p>

<h1 align="center" style="letter-spacing: 1px;">
  Building a 3D Graphics Scene Using WebGL
</h1>

<p align="center">
  <strong>Vasileios Evangelos Athanasiou</strong><br>
  Student ID: 19390005
</p>

<p align="center">
  <a href="https://github.com/Ath21" target="_blank">GitHub</a> ·
  <a href="https://www.linkedin.com/in/vasilis-athanasiou-7036b53a4/" target="_blank">LinkedIn</a>
</p>

<p align="center">
  <strong>Pantelis Tatsis</strong><br>
  Student ID: 20390226
</p>

<p align="center">
  <a href="https://github.com/PanthegrammerPRO" target="_blank">GitHub</a> ·
  <a href="https://www.linkedin.com/in/pantelis-tatsis-8287852a2/" target="_blank">LinkedIn</a>
</p>

<p align="center">
  Supervisor: Panagiota Tselenti, Laboratory Teaching Staff
</p>
<p align="center">
  <a href="https://ice.uniwa.gr/en/emd_person/panagiota-tselenti/" target="_blank">UNIWA Profile</a> ·
  <a href="https://www.linkedin.com/in/panagiotatselenti" target="_blank">LinkedIn</a>
</p>


<p align="center">
  Athens, January 2024
</p>

---

# Project Overview

This project demonstrates the incremental development of a **3D graphics environment using WebGL**. It was developed as a semester project for the **Computer Graphics** course at the **University of West Attica (UNIWA)**.  
The implementation progresses through multiple stages, starting from basic geometric primitives and evolving into an interactive, animated, and textured 3D scene.

---

## Table of Contents

| Section | Folder / File | Description |
|------:|---------------|-------------|
| 1 | `assign/` | Project assignment material |
| 1.1 | `assign/project_2023-2024.pdf` | Assignment description in English |
| 1.2 | `assign/εργασία_2023-2024.pdf` | Assignment description in Greek |
| 2 | `docs/` | Project documentation |
| 2.1 | `docs/3D-Graphics-Scene-using-WebGL.pdf` | Documentation in English |
| 2.2 | `docs/3D-Σκηνή-με-WebGL.pdf` | Documentation in Greek |
| 3 | `src/` | WebGL source code and assets |
| 3.1 | `src/textures/` | Texture images used in the 3D scenes |
| 3.1.1 | `Chair_Texture.jpg` | Chair texture |
| 3.1.2 | `Floor_Texture.jpg` | Floor texture |
| 3.1.3 | `Skybox_Texture.jpg` | Skybox texture |
| 3.1.4 | `Table_Texture.jpg` | Table texture |
| 3.2 | `src/WebGL-Libraries/` | External WebGL helper libraries |
| 3.2.1 | `gl-matrix-min.js` | Matrix and vector mathematics library |
| 3.2.2 | `webgl-debug.js` | WebGL debugging utilities |
| 3.3 | `src/1st_scene.html` | First WebGL 3D scene |
| 3.4 | `src/2nd_scene.html` | Second WebGL 3D scene |
| 3.5 | `src/3rd_scene.html` | Third WebGL 3D scene |
| 3.6 | `src/4th_scene.html` | Fourth WebGL 3D scene |
| 4 | `README.md` | Repository overview and usage instructions |

---

## Technical Features

### Scene 1: Foundations

- **Cube Formation:**  
  Implementation of a 3D cube using vertex buffers and color buffers.

- **Camera Control:**  
  Integration of `lookAt()` and `perspective()` functions to define the camera position and viewing frustum.

- **User Interface:**  
  Text input fields allow manual entry of viewing angles and orthogonal distances, accompanied by a **Redraw** button that updates the rendered scene in real time.

---

### Scene 2: Geometric Transformations

- **Object Modeling:**  
  Transformation of the initial cube into more complex composite objects, including:
  - Table  
  - Stool  
  - Chair  

- **Matrix Operations:**  
  Extensive use of transformation matrices such as:
  - `fromTranslation()`  
  - `fromScaling()`  
  - `multiply()`  

  These operations enable precise assembly of multi-part objects from simple geometric components.

---

### Scene 3: Animation and Realism

- **Dynamic Motion:**  
  Start and pause controls allow users to activate or stop camera rotation. Rotation is implemented using trigonometric functions (`Math.cos()` and `Math.sin()`).

- **Texture Mapping:**  
  Basic vertex colors are replaced with realistic textures (512×512 JPEG format), significantly improving visual realism.

---

### Scene 4: Environment and Interaction

- **World Building:**  
  A **Skybox** is implemented as the background environment, along with a 2D floor that displays the developers’ names.

- **Mouse Interaction:**  
  - Mouse movement controls the animation speed.  
  - Mouse wheel input allows the user to tip the chair forward.

- **Easter Egg:**  
  A hidden feature spawns a second chair after the main chair has been tipped over **three times**, adding an element of interactivity and discovery.

---

## Challenges and Solutions

- **Buffer Alignment:**  
  Considerable testing was required to ensure that individual object components (e.g., table legs, chair back) aligned correctly without visible gaps.

- **Texture Loading Issues:**  
  Problems where objects rendered as black were resolved by:
  - Ensuring texture images had **power-of-two dimensions**  
  - Correctly configuring texture buffers and parameters in WebGL

- **Interaction Physics:**  
  Mouse wheel logic was refined to restrict chair rotation between **0° and 90°**, preventing the model from clipping through the floor.

---

## Conclusion

This project showcases a step-by-step approach to building a fully interactive 3D WebGL scene. Through progressive development, it combines geometric modeling, transformations, animation, texture mapping, and user interaction, providing a solid practical foundation in modern computer graphics programming.

---

# Installation and Run Guide

This project is a **pure WebGL (HTML + JavaScript)** application and does **not require compilation** or external build tools.  
It runs directly in a modern web browser with **WebGL support**.

---

## Prerequisites

Before running the project, ensure the following requirements are met.

### Software Requirements
- **Modern Web Browser** with WebGL enabled:
  - Google Chrome 
  - Mozilla Firefox (recommended)
  - Microsoft Edge
- **Local HTTP Server (required for texture loading)**

> **Important**  
> Due to browser security restrictions, WebGL **cannot load textures correctly** when HTML files are opened directly (`file://`).  
> A **local web server is mandatory**.

---

## Repository Setup

### Clone the Repository

```bash
git clone https://github.com/Computer-Graphics-aka-Uniwa/Table-Chair.git
```

Alternatively, download the repository as a ZIP archive and extract it locally.

### Running the Project
Option 1: Using VS Code Live Server (Recommended)
1. Open the project folder in Visual Studio Code
2. Install the Live Server extension
3. Navigate to:
```bash
src/*_scene.html
```
4. Right-click the file and select "Open with Live Server"
5. The scene you chose will open automatically in your default browser

### Using Node.js HTTP Server

If Node.js is installed:
```bash
npm install -g http-server
cd Table-Chair/src
http-server
```
Open the displayed local URL and load the scene you desire.

## Controls and Interaction

### Scene 1

Camera Controls

- **View Angle**  
  Adjusts the camera’s field of view (degrees)

- **Orthogonal Distance**  
  Controls the distance of the camera from the scene center

- **Camera Position (Radio Buttons)**  
  Select predefined camera viewpoints around the object

- **Redraw**  
  Re-renders the scene with the selected parameters

Interaction Notes

- Scene 1 is static and does not support animation
- No mouse interaction is required
- Camera changes apply immediately after redraw

### Scene 2

Camera Controls

- **View Angle**  
  Adjusts the camera’s field of view (degrees)

- **Orthogonal Distance**  
  Controls the distance of the camera from the scene center

- **Camera Position (Radio Buttons)**  
  Select predefined camera viewpoints

- **Redraw**  
  Re-renders the scene with the selected parameters

Interaction Notes

- Scene 2 remains static
- The table and chair are positioned using fixed transformations
- No real-time interaction or animation is present

### Scene 3

Camera Controls

- **View Angle**  
  Adjusts the camera’s field of view (degrees)

- **Orthogonal Distance**  
  Controls the distance of the camera from the scene center

- **Camera Position (Radio Buttons)**  
  Select predefined camera viewpoints

- **Redraw**  
  Re-renders the scene with the selected parameters

Interaction Notes

- Scene 3 introduces textured objects but remains static
- No mouse-based interaction is required
- Texture changes are loaded automatically on scene initialization


### Scene 4

Camera Controls

- **Mouse Drag**
  Horizontal movement → Rotate camera around the scene
  Vertical movement → Move camera height (Z-axis)

- **Mouse Wheel**
  Tilt the chair forward and backward (0°–90°)

- **UI Controls**
  View Angle: Adjusts the camera’s field of view (degrees)
  Orthogonal Distance: Controls camera distance from the scene center
  Camera Position (Radio Buttons): Select predefined camera viewpoints
  Redraw: Re-renders the scene with the selected parameters
  Start / Stop: Enables or disables automatic camera rotation

## Textures

### Texture and Asset Notes
All textures are located in:
```bash
src/textures/
```
Texture characteristics:
- JPEG format
- Power-of-two dimensions (e.g., 512×512)

These constraints ensure:
- Correct mipmap generation
- Prevention of black-texture rendering issues in WebGL

## Issues and Evaluation

### Scene appears black or textures do not load
- Ensure the project is served via HTTP, not opened directly as a file.

### Mouse interaction not responding
- Click inside the canvas first to activate mouse focus.

### WebGL not supported error

- Verify WebGL is enabled in your browser:

  - Chrome: `chrome://gpu`
  - Firefox: `about:support`

### Tested Successfully On

- Mozilla Firefox

### Notes for Academic Evaluation

- No external frameworks were used
- All transformations, animations, textures, and interactions are implemented using:
  - `Raw WebGL API`
  - `glMatrix library`

The project fully complies with the Computer Graphics course requirements at UNIWA

---

## Open the Documentation
1. Navigate to the `docs/` directory
2. Open the report corresponding to your preferred language:
    - English: `3D-Graphics-Scene-using-WebGL.pdf`
    - Greek: `3D-Σκηνή-με-WebGL.pdf`