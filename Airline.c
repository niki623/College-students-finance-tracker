#include <stdio.h>
#include <string.h>
#include <stdlib.h> // for system("clear")
#include <ctype.h>  // for toupper()

#define MAX_SEATS 23
#define MAX_BOOKINGS 100

//flight details arrays
char flight_no[5][10] = {"FL123", "FL456", "FL789", "FL025", "FL684"};
char departure[5][20] = {"Manila", "Manila", "Cebu", "Clark", "Manila"};
char arrival[5][20] = {"Cebu", "Davao", "Davao", "Narita", "Incheon"};
int available_seats[5] = {MAX_SEATS, MAX_SEATS, MAX_SEATS, MAX_SEATS, MAX_SEATS};
char departureTime[5][20] = {"06:00 AM", "03:30 PM", "11:00 AM", "03:15 AM", "02:00 PM"};
char arrivalTime[5][20] = {"07:30 AM", "04:15 PM", "12:45 PM", "09:30 AM", "06:30 PM"};
float price[5] = {4998, 4231, 3678, 15945, 8643};

//booking details arrays
char booked_flight_no[MAX_BOOKINGS][10];
float booked_price[MAX_BOOKINGS];
char payment_method[MAX_BOOKINGS][10];
float booked_discount[MAX_BOOKINGS];
int booked_seats[MAX_BOOKINGS]; 

//function prototypes
void login();
void displayFlights(int size);
int reserveTicket(int size, int booking_count);
float applyDiscount(float price, int discount_type);
void generateReceipt(int booking_count);

void enter_to_continue() {
    printf("Press Enter to continue...");
    getchar();
    getchar(); //wait for Enter
}

//main function
int main() {
    int flight_count = 5;
    int choice;
    int booking_count = 0;

    login();
    system("clear"); //clear screen after successful login

    do {
        system("clear"); //clear screen before showing flights
        displayFlights(flight_count);
        booking_count = reserveTicket(flight_count, booking_count);

        int valid_input = 0;  //to check input validity
        while (!valid_input) {
            printf("Do you want to book another ticket? (1-Yes, 0-No): ");
            scanf("%d", &choice);

            if (choice == 1 || choice == 0) {
                valid_input = 1; // if a valid input is entered, set valid_input to 1 (true)
            } else {
                printf("Invalid choice! Please enter 1 for Yes or 0 for No.\n"); //else, continue loop
            }
        }
    } while (choice == 1);

    if (booking_count > 0) {
        printf("\n--- FINAL TRANSACTION SUMMARY ---\n");
        generateReceipt(booking_count);
    }

    printf("Thank you for using the Airline Reservation System!\n");
    return 0;
}

//login function
void login() {
    char username[20], password[20];
    do {
        printf("\nEnter USERNAME: ");
        scanf("%s", username);
        printf("Enter PASSWORD: ");
        scanf("%s", password);

        if (strcmp(username, "STUDENT") != 0 || strcmp(password, "TAFT2401") != 0) {
            printf("Invalid credentials! Try again.\n");
            printf("Press Enter to continue...");
            while(getchar() != '\n');
            getchar(); //wait for Enter
            system("clear");   //clear screen
        }
    } while (strcmp(username, "STUDENT") != 0 || strcmp(password, "TAFT2401") != 0);

    printf("Login successful!\n");
    enter_to_continue();
}

//function to display flight info
void displayFlights(int size) {
    printf("\nAvailable Flights:\n");
    printf("--------------------------------------------------------------------------------------------------\n");
    printf("%-6s %-10s %-10s %-10s %-10s %-16s %-16s %-10s\n", "Code", "Flight", "From", "To", "Seats", "Departure Time", "Arrival Time", "Price");
    printf("--------------------------------------------------------------------------------------------------\n");
    for (int i = 0; i < size; i++) {
        printf("%02d     %-10s %-10s %-10s %-10d %-16s %-14s PHP %.2f\n", i + 1, flight_no[i], departure[i], arrival[i], available_seats[i], departureTime[i], arrivalTime[i], price[i]);
    }
    printf("--------------------------------------------------------------------------------------------------\n");
}

//function to make a booking(input flight number and number of seats, generate receipt for the individual booking)
int reserveTicket(int size, int booking_count) {
    char flight_code_input[3];
    int selected_index = -1;

    printf("\nEnter Flight Code to reserve (e.g., 01, 02): ");
    scanf("%s", flight_code_input);

    //convert input to integer index
    if (strlen(flight_code_input) == 2 && flight_code_input[0] >= '0' && flight_code_input[1] >= '0') {
        int code = atoi(flight_code_input);
        if (code >= 1 && code <= size) {
            selected_index = code - 1;
        }
    }

    if (selected_index == -1) { //for invalid flight code
        printf("Invalid flight code!\n");
        enter_to_continue();
        return booking_count;
    }

    if (available_seats[selected_index] <= 0) { //for full flights
        printf("No available seats for this flight.\n");
        enter_to_continue();
        return booking_count;
    }

    //ask the user how many seats they want to book
    int seats_to_book = 0;
    int valid_seat_input = 0;
    while (!valid_seat_input) {
        printf("Enter number of seats to book (1-%d): ", available_seats[selected_index]);
        scanf("%d", &seats_to_book);

        //check if the input is valid
        if (seats_to_book >= 1 && seats_to_book <= available_seats[selected_index]) {
            valid_seat_input = 1; //valid input
        } else {
            printf("Invalid number of seats. Please enter a number between 1 and %d.\n", available_seats[selected_index]);
        }
    }

    //update the available seats after booking
    available_seats[selected_index] -= seats_to_book;

    //apply discount
    int discount_type = 0;
    float final_price = applyDiscount(price[selected_index], discount_type);

    //get payment method
    int valid_input = 0;
    char payment_method_input[10];
    while (!valid_input) {
        printf("\nEnter Payment Method (Cash/Card): ");
        scanf("%s", payment_method_input);

        //convert input to uppercase
        for (int i = 0; payment_method_input[i] != '\0'; i++) {
            payment_method_input[i] = toupper(payment_method_input[i]);
        }

        //checking if it is a valid payment method
        if (strcmp(payment_method_input, "CASH") == 0 || strcmp(payment_method_input, "CARD") == 0) {
            valid_input = 1;
            printf("Payment method accepted: %s\n", payment_method_input);
        } else {
            printf("We only accept CASH or CARD payment.\n");
        }
    }

    //store the booking details in arrays
    strcpy(booked_flight_no[booking_count], flight_no[selected_index]);
    booked_price[booking_count] = final_price;
    booked_discount[booking_count] = price[selected_index] - final_price;
    strcpy(payment_method[booking_count], payment_method_input);
    booked_seats[booking_count] = seats_to_book;
    booking_count++;

    //generate receipt for individual booking
    printf("\n--------- BOOKING RECEIPT ---------\n");
    generateReceipt(booking_count);

    enter_to_continue();
    system("clear"); //clear screen before next booking

    return booking_count;
}

//function to apply and calculate discount
float applyDiscount(float price, int discount_type) {
    float discount = 0;

    printf("\nDiscount Options:\n1. No Discount\n2. Senior Citizen/PWD (20%%)\n3. Manager's Discount (30%%)\nEnter choice: ");
    scanf("%d", &discount_type);

    //calculate discount
    if (discount_type == 2) discount = 0.20 * price;
    else if (discount_type == 3) discount = 0.30 * price;
    else if (discount_type == 1) discount = 0;
    else printf("Invalid input entered. Discount is set to PHP 0.00\n");

    return price - discount; //return discounted price
}

//function to generate receipt 
void generateReceipt(int booking_count) {
    float total_cost = 0;

    for (int i = 0; i < booking_count; i++) {
        float original_price = booked_price[i] + booked_discount[i];
        float total_final_price = booked_price[i] * booked_seats[i];

        printf("\n%-17s   %15s\n", "Flight Number", booked_flight_no[i]);
        printf("%-17s   %15d\n", "Seats Booked", booked_seats[i]);
        printf("%-17s   %15.2f\n", "Original Price", original_price);
        printf("%-17s   %15.2f\n", "Discount per Seat", booked_discount[i]);
        printf("%-17s   %15.2f\n", "Final Price/Seat", booked_price[i]);
        printf("%-17s   %15.2f\n", "Total Price", total_final_price);
        printf("%-17s   %15s\n", "Payment Method", payment_method[i]);
        printf("------------------------------------\n");

        total_cost += total_final_price;
    }

    printf("\n%-17s   %15.2f\n", "TOTAL AMOUNT PAID", total_cost);
    printf("------------------------------------\n\n");
}
