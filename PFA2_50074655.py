# Polling station program for PFA2
# Connor Charnock 50074655
import time


def setup_votes_file(polling_station):
    # Function to set up the file for the polling station that will store each user's votes
    try:
        filename = f"{polling_station}.txt"
        with open(filename, "x") as file:       # Exclusive creation mode to be able to raise errors
            file.write("0\n0\n0\n0\n0\n0\n0\n0\n")      # Writes 7 empty lines that will be overwritten
            print("...Generating")
            time.sleep(1)
            print(f"File setup for {polling_station}\n")
    except FileExistsError:
        # Exception handling for 'file already exists'
        print("\n** Error **")
        time.sleep(1)
        print(f"\nVotes file already exists for {polling_station}.")
        # User input to give the program administer a choice to overwrite the existing file
        overwrite = input("Do you want to overwrite the existing file? (yes/no): ").lower()
        if overwrite == "yes":
            try:
                with open(filename, "w") as file:
                    file.write("0\n0\n0\n0\n0\n0\n0\n0\n")
                print("Generating..\n")
                time.sleep(3)
                print(f"Votes file for {polling_station} has been overwritten.\n")
            except Exception:
                print("An error occurred while overwriting the votes file")
        else:       # If user inputs "No" or anything else it will abort this process
            print("Votes file setup aborted.")
    except Exception:       # Exception handling for any error that might occur during this process
        print("An error occurred while setting up the votes file")


def read_votes_from_file(polling_station):
    # Function to read votes and gender counts from the votes file.
    try:
        with open(f"{polling_station}.txt", "r") as file:
            lines = file.readlines()
        # Grabs the first 5 lines of values and converts them to a float and stores them in the votes list
        votes = [float(line.strip()) for line in lines[:5]]
        # Grabs the male and female votes from the file and stores them in these variables as integers
        male_count, female_count = map(int, lines[5:7])
        return votes, male_count, female_count
    except FileNotFoundError:
        # Exception handling for whenever a user tries entering the polling station without
        # setting up the votes file first.
        print("Polling station file not found. Please set up the votes file first.")
        return      # Returns nothing and terminates process
    except Exception:   # Exception handling for any errors occurred in this function
        print("An error occurred while reading votes from file")
        return      # Returns nothing and terminates process


def write_votes_to_file(polling_station, votes, male_count, female_count):
    # Function to write votes and gender counts to the votes file.
    try:
        with open(f"{polling_station}.txt", "w") as file:   # Using with statement, so I don't have to close the file.
            for vote in votes:
                file.write(f"{vote}\n")
            file.write(f"{male_count}\n{female_count}")  # Writes male and female votes to the file
    except Exception:
        # Exception handling for any errors occurred in this function
        print("An error occurred while writing votes to file")


def enter_polling_booth(polling_station):
    # Function that contains the code for where users enter their votes
    try:
        while True:
            existing_votes = read_votes_from_file(polling_station)
            if not existing_votes:
                return

            votes, male_count, female_count = existing_votes
            gender = input("Enter your gender male female (M/F): ").lower()     # Gender input forced into lower caps

            if gender not in ["m", "f"]:    # Exception handling for incorrect gender
                print("Error: Please enter either 'm' or 'f'.")
                return

            # Candidates contained in a list
            candidates = ["Blue Party - Bert Navy", "Green Party - Luke Lime", "Orange Party - Sally Tangerine",
                          "Red Party - Rose Burgundy", "Yellow Party - Edward Yoke"]

            votes_checker = []  # Duplicate checking list

            for i in range(len(candidates)):
                while True:
                    try:
                        vote_input = input(f"Vote for {candidates[i]} (0-5, press Enter for 0): ").strip()

                        if not vote_input:
                            vote = 0
                        else:
                            vote = float(vote_input)
                            # Exception handling for vote outside allowed value
                            if vote < 0 or vote > 5 or not vote.is_integer():
                                print("Invalid vote. Please enter a valid value between 0 and 5.")
                                continue

                        if vote == 0 or vote not in votes_checker:
                            votes_checker.append(vote)     # Vote duplication exception handling
                            break
                        else:
                            print("Duplicate vote. Please enter a different vote.")

                    except ValueError:
                        print("Invalid input. Please enter a valid value (0-5).")

                if vote != 0:
                    # Nested if statement for user vote's value.
                    if vote == 1:
                        votes[i] += 1
                    elif vote == 2:
                        votes[i] += 0.5
                    elif vote == 3:
                        votes[i] += 0.33
                    elif vote == 4:
                        votes[i] += 0.25
                    elif vote >= 5:
                        votes[i] += 0.2

            # gender input stored in variable
            if gender == "m":
                male_count += 1
            else:
                female_count += 1

            write_votes_to_file(polling_station, votes, male_count, female_count)
            print("Vote recorded\n")

            # User input chooses whether to continue voting
            while True:
                continue_voting = input("Do you want to continue voting? (yes/no): ").lower()
                if continue_voting in ["yes", "no"]:
                    break
                else:
                    # Exception handling for incorrect input
                    print("Error: Please enter either 'yes' or 'no'.")

            if continue_voting == "no":
                while True:
                    # To exit the voting poll and view statistic, the administrator should enter the password which
                    # is the same as the polling station
                    password = input("Enter the password, or 'Q' to exit: ")
                    if password == polling_station:
                        return  # Exit the function if the password is correct
                    elif password.lower() == 'q':
                        exit()  # Exit the program if 'Q' is entered
                    else:
                        print("Incorrect password. Try again.")  # Exception handling for incorrect password

    except Exception:
        print("An error occurred during the polling booth process")


def display_votes_tally(polling_station, ascending=True):
    # Function to display the votes tally for each candidate.
    try:
        candidates = ["Blue Party - Bert Navy", "Green Party - Luke Lime", "Orange Party - Sally Tangerine",
                      "Red Party - Rose Burgundy", "Yellow Party - Edward Yoke"]

        with open(f"{polling_station}.txt", "r") as file:
            lines = file.readlines()
        # Retrieves and converts the first 5 lines of values from the votes file
        # assigning the result to the 'votes' list.
        votes = [float(line.strip()) for line in lines[:5]]
        # Creates a sorted list of candidates based on their corresponding vote values.
        sorted_candidates = [candidate for _, candidate in sorted(zip(votes, candidates), reverse=not ascending)]

        print("\nVotes Tally:")
        # Goes through the sorted list of candidates and prints each candidate's name along with their vote count
        # from the 'votes' list using the index of the candidate in the original 'candidates' list.
        for candidate in sorted_candidates:
            print(f"{candidate}: {votes[candidates.index(candidate)]}")

    except FileNotFoundError:
        print("Polling station file not found. Please set up the votes file first.")
    except Exception:
        print(f"An error occurred while displaying votes tally.")


def display_overall_winner(polling_station):
    # Function to display the overall winner and their percentage share of the total votes.
    try:
        # Candidates in order stored in a list to be retrieved when calculating the winner
        candidates = ["Blue Party - Bert Navy", "Green Party - Luke Lime", "Orange Party - Sally Tangerine",
                      "Red Party - Rose Burgundy", "Yellow Party - Edward Yoke"]

        with open(f"{polling_station}.txt", "r") as file:
            lines = file.readlines()
        # Grabs and converts the first 5 lines of values from the votes file to a list of floats
        votes = [float(line.strip()) for line in lines[:5]]

        # Winner is grabbed by the index of the max value of votes
        winner = candidates[votes.index(max(votes))]
        # Percentage calculation
        percentage = (max(votes) / sum(votes)) * 100

        # Overall winner print to users terminal
        print(f"\nOverall Winner: {winner} with {percentage:.2f}% of the total votes")

    except FileNotFoundError:
        print("Polling station file not found. Please set up the votes file first.")
    except Exception:
        print("An error occurred while displaying the overall winner")


def display_gender_percentage(polling_station):
    # Function to display the percentage breakdown of male to female votes.
    try:
        with open(f"{polling_station}.txt", "r") as file:
            lines = file.readlines()
        # Retrieve the counts of male and female votes from lines 5 and 6 of the votes file, then assigns
        # them as integers to male_count and female_count
        male_count, female_count = map(int, lines[5:7])

        total_votes = male_count + female_count
        # Percentage calculations
        male_percentage = (male_count / total_votes) * 100
        female_percentage = (female_count / total_votes) * 100

        print(f"\nGender Breakdown:")
        print(f"Male: {male_percentage:.2f}%")
        print(f"Female: {female_percentage:.2f}%")

    # Exception handling for file not found, user is directed to create votes file
    except FileNotFoundError:
        print("Polling station file not found. Please set up the votes file first.")
    except Exception:
        print(f"An error occurred while displaying gender percentage")


def review_statistics(polling_station):
    # Function to review various statistics and voting analysis options.
    try:
        with open(f"{polling_station}.txt", "r") as file:
            file.readlines()
    except FileNotFoundError:
        print("Polling station file not found. Please set up the votes file first.")
        return
    except Exception:
        print("An error occurred while reading statistics")
        return

    while True:
        # Review statistics menu
        print("\n\tReview Statistics - Votes Analysis")
        print("\t**********************************\n")
        print("\t\t1. Display votes tally (ordered by party name)")
        print("\t\t2. Display votes tally (ordered in descending order of votes)")
        print("\t\t3. Overall winner, with percentage share of the total votes")
        print("\t\t4. Percentage breakdown of male to female split")
        print("\t\t5. Return to main menu\n")

        # User input choice
        option = input("Enter menu option: ")

        # If statements for the users choice
        if option == "1":
            display_votes_tally(polling_station, ascending=True)
        elif option == "2":
            display_votes_tally(polling_station, ascending=False)
        elif option == "3":
            display_overall_winner(polling_station)
        elif option == "4":
            display_gender_percentage(polling_station)
        elif option == "5":
            break
        else:      # Exception handling for choice outside allowed value
            print("Invalid option. Please enter a number between 1 and 5.")


def main():
    # Main function to run the voting poll program.
    polling_station = "Belfast_southeast"
    while True:
        # Menu board the user will see initially
        print("\n\tNI Electoral System")
        print("\t*******************\n")
        print("\t\t1. Setup polling station votes file")
        print("\t\t2. Enter polling booth")
        print("\t\t3. Review statistics")
        print("\t\t4. Exit\n")

        # User input to chose from the valid options
        option = input("Enter menu option: ")

        # If statements to control which function the program brings the user to
        if option == "1":
            setup_votes_file(polling_station)
        elif option == "2":
            enter_polling_booth(polling_station)
        elif option == "3":
            review_statistics(polling_station)
        elif option == "4":
            time.sleep(1)
            print("\n*********************")
            print("\nExiting program, Bye!")
            print("\n*********************")
            break
        else:
            # Exception handling for incorrect option choice
            print("Invalid option. Please enter a number between 1 and 4.")


# Calls the main function to start the program
main()
