#include <vector>
#include <iostream>
#include <cmath>
#include <fstream>
#include <algorithm>
#include <limits>
#include <string>

struct Angles
{
    double alpha;
    double beta;
};

// The calculate function that performs the rolling window angle calculation.
void calculate_rolling_window(const std::vector<double> &price_changes, int window_size, std::vector<Angles> &result)
{
    int n = price_changes.size();
    result.resize(n); // Resize the result vector to match the input size.

    for (int i = 0; i < n; ++i)
    {
        double min_slope = std::numeric_limits<double>::max();
        double max_slope = -min_slope;

        // Loop to find min and max slopes in the window ending at the current price change.
        for (int j = std::max(i - window_size + 1, 0); j < i; ++j)
        {
            // Calculate slope between the current point and a point in the window.
            double slope = (price_changes[i] - price_changes[j]) / (i - j);

            min_slope = std::min(min_slope, slope);
            max_slope = std::max(max_slope, slope);
        }

        // When there's at least one point in the window, calculate the angles.
        if (i > 0)
        {
            // Getting these right with what was expected was a bit confusing, first tried it
            // non-negative and swapped, but that gave wrong results compared to the correct_results.
            result[i].alpha = std::atan(-min_slope);
            result[i].beta = std::atan(-max_slope);
        }
        else
        {
            // If the window has only one point, angles are zero.
            result[i].alpha = 0;
            result[i].beta = 0;
        }
    }
}

// Reads price change data from a CSV file.
void read_csv(const std::string &filepath, std::vector<double> &data)
{
    std::ifstream file(filepath);
    double value;
    while (file >> value)
    {
        data.push_back(value);
    }
}

// Writes calculated angles to a CSV file.
void write_csv(const std::string &filepath, const std::vector<Angles> &angles)
{
    std::ofstream file(filepath);
    for (const auto &angle : angles)
    {
        file << angle.alpha << "," << angle.beta << "\n";
    }
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        std::cerr << "Usage: " << argv[0] << " <input_csv> <window_size>" << std::endl;
        return 1;
    }

    std::string input_file = argv[1];
    int window_size = std::stoi(argv[2]);
    std::vector<double> price_changes;
    std::vector<Angles> angles;

    read_csv(input_file, price_changes);

    calculate_rolling_window(price_changes, window_size, angles);

    std::string output_file = "output/window_" + std::to_string(window_size) + ".csv";
    write_csv(output_file, angles);

    return 0;
}
