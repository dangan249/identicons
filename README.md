# identicons

### Introduction
Thank you for spending time reviewing my project.  I hope you will enjoy it as much as I have.

### Identicon objectives:
* The image is drawn in a 5X5 grid (each cell has 25 pixels) 
* Each unique input string will result in a unique identicon.   
* My strategy to make the identicon looks aesthetically pleasing is to make sure there is enough white cells to act as background.  I also implement both horizontal and vertical symmetry.

![identicon_jane_1723598650](https://github.com/user-attachments/assets/0e5fd602-a474-4e91-8c48-bce70e5d9a0d)
![identicon_john_1723598657](https://github.com/user-attachments/assets/b2b56661-6c62-4c01-8903-a53d4664026f)
![identicon_931D387731bBbC988B31220_1723598647](https://github.com/user-attachments/assets/a5892374-0d20-4320-afa2-09daede78145)


### Implementation details:
* The input string is converted to a unique 600 bits binary string.  Each 24 bits in that binary string is used to generate an RGB color for each cell.  
* I use numpy to create a (5,5,3) matrix and rely on numpy's vectorization functions to transform the matrix.

### Run instructions:

You can run the project as a regular Python project or run every thing inside a Docker container like my below preferred workflow.  

1. **Install Docker and a container runtime (Docker Dekstop or Colima) for MacBook:**

  Docker installation for MacBook

    brew install --cask docker

  Colima is simple to install too:

    brew install colima
    https://github.com/abiosoft/colima


  We will use colima to provision a runtime for Docker

    colima start --cpu 2 --memory 4

2. **Build and Run the project**
```bash
docker build . -t identicons
docker run -it -v $(pwd):/app identicons --username john
```
