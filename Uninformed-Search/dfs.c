/*
    URI Judge Problem No 3247 - Robots on a Grid
*/

#include <stdio.h>
#include <stdlib.h>

enum color {white, grey, black};

typedef struct boardT{
    int walkable;
    int tileColor;
}boardT;

unsigned long int pathNum;

/* 
    Basic traverse traverse's the board walking only down and right
    Increments pathNum whenever a new path from s to t is found
*/
int basicTraverse(boardT **board, int currCol, int currRow, int size){
    int rightPath = 0, downPath = 0;
    //printf("%d;%d\n", currCol, currRow);

    if(currCol == size-1 && currRow == size-1){
        pathNum++;
        return 1;
    }else{
        if(currCol+1 < size &&
            board[currCol+1][currRow].walkable == 1 && 
                board[currCol+1][currRow].tileColor == white){
                    downPath = basicTraverse(board, currCol+1, currRow, size);
        }else if(currCol+1 < size && board[currCol+1][currRow].tileColor == grey){
            pathNum++;
            downPath = 1;
        }

        if(currRow+1 < size &&
            board[currCol][currRow+1].walkable == 1 && 
                board[currCol][currRow+1].tileColor == white){
                    rightPath = basicTraverse(board, currCol, currRow+1, size);
        }else if(currRow+1 < size && board[currCol][currRow+1].tileColor == grey){
            pathNum++;
            rightPath = 1;
        }

        if(rightPath == 1 || downPath == 1){
            board[currCol][currRow].tileColor = grey;
        }else{
            board[currCol][currRow].tileColor = black;
        }
    
    }
    
    return (rightPath || downPath);
}

/* 
    Incremented traverse traverse's the board walking up, down, left and right
    Return 1 when path is found, returns -1 if no path is found
*/
void incrementedTraverse(boardT **board, int currCol, int currRow, int size){
    //printf("%d;%d\n", currCol, currRow);

    if(currCol == size-1 && currRow == size-1){
        printf("THE GAME IS A LIE\n");
        pathNum = -1;
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

    if(pathNum != 0){
        printf("%ld\n", pathNum%2147483647);
    }else{
        for(i = 0; i < size; i++){
            for(j = 0; j < size; j++){
                board[i][j].tileColor = white;
            }
        }
        incrementedTraverse(board, 0, 0, size);
        if(pathNum != -1){
            printf("INCONCEIVABLE\n");
        }
    }
    

    return 0;
}