<div align= >

# <img align=center width=75px height=75px src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWh0OTEyb2JzajB6OGUxY2xiYzcwM2EycDAydXNzYjloMzg5b21jaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/16RQhnWiTDny1DHcNN/giphy.gif"> OTP Stream Cipher
</div>
<div align="center">
   <img align="center" height=100% src="./docs/crypto-project.excalidraw.png" alt="system architecture">
</div>



<p align="center"> 
    <br> 
</p>

## <img align= "center" width=50px src="https://media4.giphy.com/media/xN3IbsXsm1pOtGOkx2/giphy.gif?cid=ecf05e47lnbd6mvq1joc1wjqtdh7aonlxeiin9t26d7qgrh1&ep=v1_stickers_search&rid=giphy.gif&ct=s"> Table of Contents

- <a href ="#about"> 📙 Overview</a>
- <a href ="#features"> ✨ Features</a>
- <a href ="#usage"> 🛠️ Usage</a>
- <a href ="#contributors"> ✨ Contributors</a>
- <a href ="#license"> 🔒 License</a>
<hr style="background-color: #4b4c60"></hr>

<a id = "about"></a>

## <img align="center"  height =50px src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3FwejRnc3g0eWF5cWdzNmc3Nm03cGdzNDAxbTZ6bGc4MDZ6emd0byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/VMXbE5DJU4F5D986f3/giphy.gif"> Overview

<br>
<ul> 
<li>One-Time Pad (OTP) Stream Cipher system.</li>
<li>It includes encryption, decryption, and secure key exchange using Diffie-Hellman.</li>
</ul>
<hr style="background-color: #4b4c60"></hr>

<a id="features"></a>

## <img align= "center" width=50px src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2d4cmltanJuNnp2MG92NGlnN2pzczZ1em0yZmRrczE0M3VpMXo2eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/jTUai5xFuOj9gmG981/giphy.gif"> Features

<ul>
<li>Secure key exchange using Diffie-Hellman algorithm.</li>
<li>Stream cipher encryption and decryption using Linear Congruential Generator (LCG).</li>
<li>Seed encryption using AES for secure transmission.</li>
<li>HMAC-based authentication for data integrity.</li>
<li>Socket-based communication for data transfer.</li>
</ul>

<hr style="background-color: #4b4c60"></hr>

<a id="usage"></a>

## <img align= "center" width=50px src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjZhbDVtcGJyMjUyaG0wZXYyNTdsenRvajF6MTc5eXIwM29mZmVjdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/IOaLEhOlGiuwDRqgul/giphy.gif"> Usage



### Running the System

1. **Sender Mode**:

   ```bash
   python main.py sender  --input data/input.txt
   ```

2. **Receiver Mode**:
   ```bash
   python main.py receiver --output data/output.txt
   ```

### Configuration

- Modify `config/config.yaml` to set network and cryptographic parameters.

<hr style="background-color: #4b4c60"></hr>

<a id ="contributors"></a>

## <img  align="center" width= 70px height =55px src="https://media0.giphy.com/media/Xy702eMOiGGPzk4Zkd/giphy.gif?cid=ecf05e475vmf48k83bvzye3w2m2xl03iyem3tkuw2krpkb7k&rid=giphy.gif&ct=s"> Contributors

<table  >
  <tr>
      <td align="center"><a href="https://github.com/amir-kedis"><img src="https://avatars.githubusercontent.com/amir-kedis?v=4" width="150px;" alt=""/><br /><sub><b>Amir Kedis</b></sub></a><br /></td>
     <td align="center"><a href="https://github.com/g-magdy"><img src="https://avatars.githubusercontent.com/g-magdy?v=4" width="150px;" alt=""/><br /><sub><b>George Magdy</b></sub></a><br /></td>
  </tr>
</table>

## 🔒 License <a id ="license"></a>

> This software is licensed under MIT License, See [License](LICENSE) for more information ©Amir.
