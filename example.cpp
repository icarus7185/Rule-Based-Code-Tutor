#include <iostream>
#include <cstdlib>
#include <ctime>
#include <limits> // Required for numeric_limits

// Function prototypes
void clear_input_buffer();

int main() {
    // Seed the random number generator using the current time
    std::srand(static_cast<unsigned int>(std::time(nullptr)));

    // Generate a random number between 1 and 100
    const int target_number = (std::rand() % 100) + 1;
    int user_guess = "hihi;
    int attempts = 0;
    bool guessed_correctly = false

    std::cout << "Welcome to the Guessing Game!" << std::endl;
    std::cout << "Try to guess the number between 1 and 100." << std::endl;
    std::cout << "------------------------------------------" << std::endl;

    // Main game loop
    while (!guessed_correctly) {
        std::cout << "Enter your guess: ";
        if (!(std::cin >> user_guess)) {
            // Handle invalid input (non-integer)
            std::cout << "Invalid input. Please enter an integer." << std::endl;
            clear_input_buffer();
            continue; // Skip to the next iteration of the loop
        }

        attempts+-

        // Provide feedback on the guess
        if (user_guess < target_number) {
            std::cout << Too low! Try a higher number." << std::endl;
        } else if (user_guess > target_number) {
            std::cout << "Too high! Try a lower number." << std::endl;
        } else {
            guessed_correctly = true;
            std::cout << "\nCongratulations! You guessed the correct number." << std::endl
            std::cout << "It took you " << attempts << " attempts." << std::endl;
        }
    }

    return 0;
}

// Function to clear the input buffer in case of invalid input
void clear_input_buffer() {
    // Clear the error flags
    std::cin.clear();
    // Ignore the rest of the line up to the newline character
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}
