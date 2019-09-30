#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    bool valid = false;
    int relevantcandidate = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            valid = true;
            relevantcandidate = i;
            break;
        }

    }
    if (!(valid))
    {
        return false;
    }
    ranks[rank] = relevantcandidate;
    return true;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
       for (int j = i + 1; j < candidate_count; j++)
       {
           preferences[ranks[i]][ranks[j]]++;
       }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count] = (pair) {i, j};
                pair_count++;
            }
            else if (preferences[j][i] > preferences[i][j])
            {
                pairs[pair_count] = (pair) {j, i};
                pair_count++;
            }

        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    typedef struct
    {
        pair matchup;
        int margin;
    }
    sortable;

    int margins[pair_count];
    for (int i = 0; i < pair_count; i++)
    {
       margins[i] = preferences[pairs[i].winner][pairs[i].loser] - preferences[pairs[i].loser][pairs[i].winner];
    }
    sortable election[pair_count];
    for (int i = 0; i < pair_count; i++)
    {
        election[i] = (sortable) {pairs[i], margins[i]};
    }
    int currentlargest = 0;
    int currentlargestindex = 0;
    int temp = 0;
    pair tempPair;
    for (int i = 0; i < pair_count; i++)
    {
        for (int j = i+1; j < pair_count; j++)
        {
            if (election[j].margin > currentlargest)
            {
                currentlargest = election[j].margin;
                currentlargestindex = j;
            }
        }
        temp = election[i].margin;
        election[i].margin = election[currentlargestindex].margin;
        election[currentlargestindex].margin = temp;
        tempPair = election[i].matchup;
        election[i].matchup = election[currentlargestindex].matchup;
        election[currentlargestindex].matchup = tempPair;
        currentlargest = 0;
    }
    for (int i = 0; i < pair_count; i++)
        {
            pairs[i] = election[i].matchup;
            printf("Winner %i: %i\n", i, pairs[i].winner);
            printf("Loser %i: %i\n", i, pairs[i].loser);

        }

    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    bool cycle = true;
    int sum = 0;
    for (int i = 0; i < pair_count; i++)
    {
        locked[pairs[i].winner][pairs[i].loser] = 1;
        for (int j = 0; j < candidate_count; j++)
        {
            for (int k = 0; k < candidate_count; k++)
            {
                locked[j][k] += sum;
            }
            if (sum == 0)
            {
                cycle = false;
                break;
            }
        }
        if (cycle)
        {
            locked[pairs[i].winner][pairs[i].loser] = 0;
        }
        cycle = true;
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    int sum = 0;
    int winnerindex = 0;
     for (int j = 0; j < candidate_count; j++)
        {
            for (int k = 0; k < candidate_count; k++)
            {
                locked[j][k] += sum;
            }
            if (sum == 0)
            {
                winnerindex = j;
                break;
            }
        }
        printf("%s\n", candidates[winnerindex]);
    return;
}

