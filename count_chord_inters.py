import ast
import matplotlib.pyplot as plt
import numpy as np
import sys

def plot_chords(radians, chords_start_end, num_intersections, axs, row, col):
    '''
    Plot the chords on the unit circle,
    given the radian measures and chord identifiers
    '''
    # Convert radian measures to (x, y) coordinates
    x = np.cos(radians)
    y = np.sin(radians)
    
    # Plot the circle
    circle = plt.Circle((0, 0), 1, color="black", fill=False)
    axs[row, col].add_patch(circle)
    axs[row, col].plot([],[])

    # Plot the chords
    for chord_start_end in chords_start_end:
        start_i = chord_start_end[0]
        end_i = chord_start_end[1]
        axs[row, col].plot([x[start_i], x[end_i]], [y[start_i], y[end_i]])

    axs[row, col].set_yticks([])
    axs[row, col].set_xticks([])
    axs[row, col].set_title("# Intersections: {0}".format(num_intersections))
    axs[row, col].set_aspect("equal")
    axs[row, col].axis("off")

def merge_count_inversions(nums, start, mid, end):
    '''
    Count inversions while merging sorted sublists in-place
    '''
    left = nums[start : mid + 1]
    right = nums[mid + 1 : end + 1]

    left_pointer = 0
    right_pointer = 0
    nums_pointer = start
    num_inversions = 0

    while left_pointer < len(left) and right_pointer < len(right):
        if left[left_pointer] <= right[right_pointer]:
            nums[nums_pointer] = left[left_pointer]
            left_pointer += 1
        else:
            # Inversion occurs where right element < left element
            num_inversions += len(left) - left_pointer
            nums[nums_pointer] = right[right_pointer]
            right_pointer += 1

        nums_pointer += 1

    # Copy remaining elements into place
    while left_pointer < len(left):
        nums[nums_pointer] = left[left_pointer]
        left_pointer += 1
        nums_pointer += 1

    while right_pointer < len(right):
        nums[nums_pointer] = right[right_pointer]
        right_pointer += 1
        nums_pointer += 1

    return num_inversions

def mergesort_count_inversions(nums, start, end):
    '''
    Count inversions via standard mergesort procedure
    '''
    num_inversions = 0

    if start < end:
        mid = (start + end) // 2
        num_inversions += mergesort_count_inversions(nums, start, mid)
        num_inversions += mergesort_count_inversions(nums, mid + 1, end)
        num_inversions += merge_count_inversions(nums, start, mid, end)

    return num_inversions

def count_inversions(nums):
    '''
    Count the inversions in a list
    '''
    return mergesort_count_inversions(nums, 0, len(nums) - 1)

def count_intersections(radians, chord_identifiers):
    '''
    Count the number of chord intersection,
    given a list of radian measures and a list of chord identifiers 
    '''
    num_chords = len(radians) // 2
    num_intersections = 0
    
    # Determine the start and end indices of each chord (for plotting)
    chords_start_end = np.zeros((num_chords, 2), dtype=int)

    # Determine order in which chords start and end
    start_end_order = []
    end_order = []

    for i, identifier in enumerate(chord_identifiers):
        chord = int(identifier[1:]) - 1
        
        # Chord interval opens
        if identifier[0] == "s":
            chords_start_end[chord][0] = i
            start_end_order.append(2 * chord)
        
        # Chord interval closes
        else:
            chords_start_end[chord][1] = i
            start_end_order.append(2 * chord + 1)
            end_order.append(chord)

    num_intersections = count_inversions(start_end_order) - 2 * count_inversions(end_order)
    return num_intersections, chords_start_end

def process_input(input_file):
    '''
    Process each input instance, counting intersections and outputting results,
    given an input file name
    '''
    try:
        with open(input_file, "r") as file:
            # Initialize plot
            num_instances = sum(1 for line in file)
            num_cols = 3
            num_rows = int(np.ceil(num_instances / num_cols))
            fig, axs = plt.subplots(num_rows, num_cols)
            file.seek(0)

            for i, line in enumerate(file):
                # Read radian measures and chord identifiers
                instance_data = ast.literal_eval(line.strip())
                radians, chord_identifiers = instance_data[0], instance_data[1]

                # Ensure valid list lengths
                if len(radians) % 2 != 0 or len(radians) != len(chord_identifiers):
                    raise ValueError("The lengths of the radian measure and chord identifiers lists must be even and equal.")

                # Count chord intersections and plot results
                num_intersections, chords_start_end = count_intersections(radians, chord_identifiers)
                row, col = i // 3, i % 3
                plot_chords(radians, chords_start_end, num_intersections, axs, row, col)

            plt.tight_layout()
            [ax.set_axis_off() for ax in axs.flatten() if not ax.has_data()]
            plt.savefig("output.png", format="png")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Ensure that an input file path is provided
    if len(sys.argv) != 2:
        print("Usage: python count_chord_ints.py input_file.txt")
        sys.exit(1)

    # Count intersections of each input instance
    input_file = sys.argv[1]
    process_input(input_file)
