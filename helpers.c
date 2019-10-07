#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    double sum = 0;
    int rounded = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // We simply add the R, G, and B values of pixel, then average
            sum = image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed;
            sum = sum / 3;
            // To convert the double to int we cast it
            rounded = (int) round(sum);
            image[i][j].rgbtBlue = rounded;
            image[i][j].rgbtGreen = rounded;
            image[i][j].rgbtRed = rounded;
        }
    }
    return;

}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Creating a new RGBTRIPLE so I can store the reflected values without losing the original as they are used in future calculations
    RGBTRIPLE dummy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // So each pixel is matched to its counterpart on the other side of the x-direction
            dummy[i][j].rgbtBlue = image[i][width - j - 1].rgbtBlue;
            dummy[i][j].rgbtGreen = image[i][width - j - 1].rgbtGreen;
            dummy[i][j].rgbtRed = image[i][width - j - 1].rgbtRed;
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // So each pixel is matched to its counterpart on the other side of the x-direction
            image[i][j].rgbtBlue = dummy[i][j].rgbtBlue;
            image[i][j].rgbtGreen = dummy[i][j].rgbtGreen;
            image[i][j].rgbtRed = dummy[i][j].rgbtRed;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE dummy[height][width];
    double blueSum = 0;
    double redSum = 0;
    double greenSum = 0;
    int redAverage = 0;
    int blueAverage = 0;
    int greenAverage = 0;
    int divisor = 9;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // This is an inner nested loop as for both the rows and columns we based the value off of pixels -1, 0, 1 away
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    // Checks If the array access would be out of bounds and skips the value call if so, also lessens divisor by 1 since you are average less values
                    if ((j + l < 0) || (j + l >= width))
                    {
                        divisor--;

                    }
                    else if ((i + k < 0) || (i + k >= height))
                    {
                        divisor--;
                    }
                    else
                    {
                        blueSum += image[i + k][j + l].rgbtBlue;
                        redSum += image[i + k][j + l].rgbtRed;
                        greenSum += image[i + k][j + l].rgbtGreen;
                    }
                }
            }
            blueAverage = (int) round(blueSum / divisor);
            redAverage = (int) round(redSum / divisor);
            greenAverage = (int) round(greenSum / divisor);
            dummy[i][j].rgbtBlue = blueAverage;
            dummy[i][j].rgbtRed = redAverage;
            dummy[i][j].rgbtGreen = greenAverage;
            // resets the values of the loop
            blueSum = 0;
            redSum = 0;
            greenSum = 0;
            divisor = 9;

        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Updates image at the end
            image[i][j].rgbtBlue = dummy[i][j].rgbtBlue;
            image[i][j].rgbtRed = dummy[i][j].rgbtRed;
            image[i][j].rgbtGreen = dummy[i][j].rgbtGreen;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    //d
    int xGradientBlue = 0;
    //s
    int xGradientRed = 0;
    //a
    int xGradientGreen = 0;
    //b
    int yGradientBlue = 0;
    int yGradientRed = 0;
    int yGradientGreen = 0;
    int singleValueBlue = 0;
    int singleValueRed = 0;
    int singleValueGreen = 0;
    // Made the dummy array extra big to create a border of all 0s
    RGBTRIPLE dummy[height + 2][width + 2];
    //l
    for (int i = 0; i < height + 2; i++)
    {
        for (int j = 0; j < width + 2; j++)
        {
            dummy[i][j].rgbtBlue = 0;
            dummy[i][j].rgbtRed = 0;
            dummy[i][j].rgbtGreen = 0;
        }
    }
    // x
    for (int i = 0; i < height + 2; i++)
    {
        for (int j = 0; j < width + 2; j++)
        {
            if (j == 0 || j == width + 1 || i == 0 || i == width + 1)
            {
                dummy[i][j].rgbtRed = 0;
                dummy[i][j].rgbtBlue = 0;
                dummy[i][j].rgbtGreen = 0;
            }
            else
            {
                dummy[i][j].rgbtBlue = image[i - 1][j - 1].rgbtBlue;
                dummy[i][j].rgbtRed = image[i - 1][j - 1].rgbtRed;
                dummy[i][j].rgbtGreen = image[i - 1][j - 1].rgbtGreen;
            }
        }
    }
    for (int i = 1; i < height + 1; i++)
    {
        for (int j = 1 ; j < width + 1; j++)
        {
            xGradientBlue = -1 * dummy[i-1][j-1].rgbtBlue + -2 * dummy[i][j-1].rgbtBlue + -1 * dummy[i+1][j-1].rgbtBlue + dummy[i-1][j+1].rgbtBlue + 2 * dummy[i][j+1].rgbtBlue + dummy[i+1][j+1].rgbtBlue;
            yGradientBlue = -1 * dummy[i-1][j-1].rgbtBlue + -2 * dummy[i-1][j].rgbtBlue + -1 * dummy[i-1][j+1].rgbtBlue + dummy[i+1][j-1].rgbtBlue + 2 * dummy[i+1][j].rgbtBlue + dummy[i+1][j+1].rgbtBlue;
            singleValueBlue = (int) round(sqrt(pow(xGradientBlue, 2) + pow(yGradientBlue, 2)));
            xGradientRed = -1 * dummy[i-1][j-1].rgbtRed + -2 * dummy[i][j-1].rgbtRed + -1 * dummy[i+1][j-1].rgbtRed + dummy[i-1][j+1].rgbtRed + 2 * dummy[i][j+1].rgbtRed + dummy[i+1][j+1].rgbtRed;
            yGradientRed = -1 * dummy[i-1][j-1].rgbtRed + -2 * dummy[i-1][j].rgbtRed + -1 * dummy[i-1][j+1].rgbtRed + dummy[i+1][j-1].rgbtRed + 2 * dummy[i+1][j].rgbtRed + dummy[i+1][j+1].rgbtRed;
            singleValueRed = (int) round(sqrt(pow(xGradientRed, 2) + pow(yGradientRed, 2)));
            xGradientGreen = -1 * dummy[i-1][j-1].rgbtGreen + -2 * dummy[i][j-1].rgbtGreen + -1 * dummy[i+1][j-1].rgbtGreen + dummy[i-1][j+1].rgbtGreen + 2 * dummy[i][j+1].rgbtGreen + dummy[i+1][j+1].rgbtGreen;
            yGradientGreen = -1 * dummy[i-1][j-1].rgbtGreen + -2 * dummy[i-1][j].rgbtGreen + -1 * dummy[i-1][j+1].rgbtGreen + dummy[i+1][j-1].rgbtGreen + 2 * dummy[i+1][j].rgbtGreen + dummy[i+1][j+1].rgbtGreen;
            singleValueGreen = (int) round(sqrt(pow(xGradientGreen, 2) + pow(yGradientGreen, 2)));
            if (singleValueBlue > 255)
            {
                singleValueBlue = 255;
            }
            if (singleValueRed > 255)
            {
                singleValueRed = 255;
            }
            if (singleValueGreen > 255)
            {
                singleValueGreen = 255;
            }
            image[i - 1][j - 1].rgbtBlue = singleValueBlue;
            image[i - 1][j - 1].rgbtGreen = singleValueGreen;
            image[i - 1][j - 1].rgbtRed = singleValueRed;
        }
    }
    return;
}
