#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    double sum = 0;
    int rounded = 0;
    for (int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            sum = image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed;
            sum = sum / 3;
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
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
