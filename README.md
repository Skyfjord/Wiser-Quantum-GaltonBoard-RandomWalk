#Quantum Galton Board Simulator: Universal Statistical Simulator Implementation

Team Name  
GOAT

Team Members  
- Member 1: Jason Gomez, gst-lw1aEEEAapaEX8L
- Member 2: Tanya Adlakha, gst-VusimuxPaOvsT6p  




Project Summary

Our project focuses on implementing a quantum version of the classical Galton Board (also known as the Plinko board) using quantum circuits, based on the framework presented in the paper *Universal Statistical Simulator* by Mark Carney and Ben Varcoe. The classical Galton Board is a simple mechanical device demonstrating the central limit theorem, where balls dropped through an array of pegs form a Gaussian distribution when collected in bins. However, classical simulations of such stochastic processes become computationally expensive as the number of levels increases.

To address this challenge, we explore a quantum computing approach to simulate the Galton Board’s behavior exponentially faster by harnessing quantum superposition and interference. The Universal Statistical Simulator introduces a quantum circuit capable of generating all possible trajectories of an n-level Galton Board simultaneously, leveraging only three types of quantum gates. This construction drastically reduces circuit depth and resource requirements compared to prior quantum walk models.

Our implementation encodes the paths of the Galton Board into quantum states using multi-controlled gates and leverages the Quantum Fourier Transform to manipulate and extract distribution information efficiently. By modifying the left-right bias at each step and removing physical peg constraints, the quantum circuit acts as a universal statistical simulator, capable of generating a variety of probability distributions beyond the classical Gaussian, such as exponential and even quantum walk distributions.

Through simulation on quantum circuit simulators and limited hardware testing, our results confirm that the quantum Galton Board effectively reproduces classical probability distributions and sets the foundation for future applications in solving high-dimensional partial differential equations and complex stochastic models in physics and engineering.

This project demonstrates the potential of quantum algorithms to outperform classical Monte Carlo simulations for certain problems, providing insights into the evolving role of quantum computing in statistical modeling. It also serves as an educational tool, illustrating how abstract quantum operations translate to real-world stochastic phenomena.

We have prepared a presentation deck summarizing our approach, implementation details, results, and future directions, aimed at conveying both the theoretical and practical aspects of the quantum Galton Board simulator.

Project Presentation Deck  
*Please find the presentation deck file attached in the repository.*
