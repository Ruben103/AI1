#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "libStateQueue.h"

/* isValid checks the validity of a potential move and returns true or false */

int isValid(State s, char** maze, int dr, int dc, int r, int c) {
	if ( (s.r + dr > r) || (s.c + dc > c ) || (s.r + dr < 0) || (s.c + dc < 0) ){
		return 0;
	}
    char ch;
    ch = maze[(s.r + dr)][(s.c + dc)]; /* the object at the location of potential move */
    if (ch == '#'){ // wall, move impossible 
		return 0;
	}
	maze[(s.r + dr)][(s.c + dc)] = '#';
    return 1;
} 

/* currentLocation prints the location of a state using the coordinates from the Lab Assignment */

void currentLocation(State s){
	switch (s.r){
	case 7:
		printf("%d\n", ((s.c + 1)/2));
		break;
	case 5:
		printf("%d\n", ((s.c + 9)/2));
		break;
	case 3:
		printf("%d\n", ((s.c + 17)/2));
		break;
	case 1:
		printf("%d\n", ((s.c + 25)/2));
		break;
	default:
		break;
	}
	return;
}

/* solveMaze creates a priority queue of states s, each representing a point in the maze
 * and the minimum amount of time steps to reach that point. New states are created if they
 * require less steps than the current best time and are valid moves. */

void solveMaze(char** maze, int r, int c, int ir, int ic, int gr, int gc) {
	int n = 0;
    State s, temp_s;
    Queue qp;
    qp = newEmptyQueue();
	s.r = ir;
	s.c = ic;
	enqueue(s, &qp); // starting position
	while(!isEmptyQueue(qp)){
		s = dequeue(&qp);
		printf("\n\nCurrent Location: ");
		currentLocation(s);
		if (s.r == gr && s.c == gc){ // goal found
			printf("Goal found\n");
			break;
		}
		// move West
		temp_s = s;
		if (isValid(s, maze, 0, -1, r, c) && isValid(s, maze, 0, -2, r, c)){
			temp_s.c--;
			temp_s.c--;
			insertUnique(temp_s, &qp);
			printf("enqueued: W ");
			currentLocation(temp_s); 
		}
		// move South
		temp_s = s;
		if (isValid(s, maze, 1, 0, r, c) && isValid(s, maze, 2, 0, r, c)){
			temp_s.r++;
			temp_s.r++;
			insertUnique(temp_s, &qp);
			printf("enqueued: S ");
			currentLocation(temp_s); 
		}
		// move East
		temp_s = s;
		if (isValid(s, maze, 0, 1, r, c) && isValid(s, maze, 0, 2, r, c)){
			temp_s.c++;
			temp_s.c++;
			insertUnique(temp_s, &qp);
			printf("enqueued: E ");
			currentLocation(temp_s); 
		}
		// move North
		temp_s = s;
		if (isValid(s, maze, -1, 0, r, c) && isValid(s, maze, -2, 0, r, c)){ 
			temp_s.r--;
			temp_s.r--;
			insertUnique(temp_s, &qp);
			printf("enqueued: N ");
			currentLocation(temp_s); 
		}
		n++;
		if (n == 10000){
			break;
		}
	}
    freeQueue(qp); // free allocated memory
    return;
}

/* main takes the following input from the user:
 * • A line containing two positive odd integers r, c, the number of rows and columns in the maze. 
 * • A line containing two positive odd integers ir, ic, the initial location in the maze.
 * • A line containing two positive odd integers gr, gc, the goal location in the maze.
 * • r lines each containing c characters, representing the maze. ‘#’ represents a wall and ‘.’ represents paths.
 */
 
int main(int argc, char *argv[]){
	int i, j;
	int r, c;
	scanf("%d %d\n", &r, &c);
	int ir, ic;
	scanf("%d %d\n", &ir, &ic);
	int gr, gc;
	scanf("%d %d\n", &gr, &gc);
	char **maze;
	maze = malloc(r * sizeof(char*));
	for (i = 0; i < r; i++){
		maze[i] = malloc(c * sizeof(char));
	}
	for (i = 0; i < r; i++){
		for (j = 0; j < c; j++){
			scanf("%c", &maze[i][j]);
		}
		getchar();
	}
	solveMaze(maze, r, c, ir, ic, gr, gc); 
	for (i = 0; i < r; i++){
		free(maze[i]);
	}
	free(maze);
  return 0;
}
