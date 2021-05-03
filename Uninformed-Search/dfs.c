/*
    URI Judge Problem No 3247 - Robots on a Grid
    Bruno Sampaio Leite
*/

#include <stdio.h>
#include <stdlib.h>

enum color {white, grey, black};

typedef struct boardT{
    int walkable;
    int tileColor;
    unsigned long long int nodePathNum;
}boardT;

unsigned long long int pathNum;
int theGameLies;

/* 
    Basic traverse traverse's the board walking only down and right;
    It keeps a table containing the number of found paths on an already explored vertex, so that
    when that vertex is found again through a new path it's not explored redundantly;
    This approach is similar to Dynamic Programming
*/
int basicTraverse(boardT **board, int currCol, int currRow, int size){
    //printf("%d;%d\n", currCol, currRow);
    int currPathNum = 0;

    if(currCol == size-1 && currRow == size-1){
        return 1;
    }else{
        board[currCol][currRow].tileColor = grey;

        if(currCol+1 < size &&
            board[currCol+1][currRow].walkable == 1 &&
                board[currCol+1][currRow].tileColor == white){
                    currPathNum += basicTraverse(board, currCol+1, currRow, size);
        }else if(currCol+1 < size && board[currCol+1][currRow].tileColor == black){
            currPathNum += board[currCol+1][currRow].nodePathNum;
        }

        if(currRow+1 < size &&
            board[currCol][currRow+1].walkable == 1 &&
                board[currCol][currRow+1].tileColor == white){
                    currPathNum += basicTraverse(board, currCol, currRow+1, size);
        }else if(currRow+1 < size && board[currCol][currRow+1].tileColor == black){
            currPathNum += board[currCol][currRow+1].nodePathNum;
        }

        board[currCol][currRow].tileColor = black;
        board[currCol][currRow].nodePathNum = currPathNum;
    }

    return currPathNum;
}

/* 
    Incremented traverse traverse's the board walking up, down, left and right;
    Sets theGameLies to 1 if a path is found;
    Simple DFS algorithm;
*/
void incrementedTraverse(boardT **board, int currCol, int currRow, int size){
    //printf("%d;%d\n", currCol, currRow);

    if(currCol == size-1 && currRow == size-1){
        theGameLies = 1;
    }else{
        board[currCol][currRow].tileColor = grey;

        if(currCol+1 < size &&
            board[currCol+1][currRow].walkable == 1 && 
                board[currCol+1][currRow].tileColor == white){
                    incrementedTraverse(board, currCol+1, currRow, size);
        }

        if(currRow+1 < size &&
            board[currCol][currRow+1].walkable == 1 && 
                board[currCol][currRow+1].tileColor == white){
                    incrementedTraverse(board, currCol, currRow+1, size);
        }

        if(currCol-1 >= 0 &&
            board[currCol-1][currRow].walkable == 1 && 
                board[currCol-1][currRow].tileColor == white){
                    incrementedTraverse(board, currCol-1, currRow, size);
        }

        if(currRow-1 >= 0 &&
            board[currCol][currRow-1].walkable == 1 && 
                board[currCol][currRow-1].tileColor == white){
                    incrementedTraverse(board, currCol, currRow-1, size);
        }

        board[currCol][currRow].tileColor = black;
    }

    return;

}

int main(){
    int size, i, j;
    char tile;
    boardT **board;

    pathNum = 0; theGameLies = 0;
    
    scanf("%d", &size);

    board = malloc(size*sizeof(boardT *));
    for(i = 0; i < size; i++){
        board[i] = malloc(size*sizeof(boardT));
    }

    for(i = 0; i < size; i++){
        tile = getchar();
        for(j = 0; j < size; j++){
            tile = getchar();
            //tile = getchar();
            board[i][j].tileColor = white;
            board[i][j].nodePathNum = 0;
            if(tile == '.'){
                board[i][j].walkable = 1;
            }else if(tile == '#'){
                board[i][j].walkable = 0;
            }else{
                printf("Non recognized symbol!\n");
                return 0;
            }
        }
    }

    basicTraverse(board, 0, 0, size);

    if(board[0][0].nodePathNum != 0){
        printf("%lld\n", board[0][0].nodePathNum%2147483647);
    }else{
        for(i = 0; i < size; i++){
            for(j = 0; j < size; j++){
                board[i][j].tileColor = white;
            }
        }
        incrementedTraverse(board, 0, 0, size);
        if(theGameLies == 1){
            printf("THE GAME IS A LIE\n");
        }else{
            printf("INCONCEIVABLE\n");
        }
    }
    return 0;
}