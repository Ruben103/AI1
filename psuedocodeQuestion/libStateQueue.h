/* LibStateQueue.h, February 2019 */

#ifndef LIBSTATEQUEUE_H
#define LIBSTATEQUEUE_H

/* a state contains the position in a maze given by it's (r,c) coordinates, the category
 * of the state (what can it pass, gate, flowerbed, etc) and the current number of steps to reach 
 * that (r,c) position */
typedef struct State {
  int r;
  int c;
} State;

/* List is the type of lists of states */
typedef struct ListNode* List;

struct ListNode {
  State item;
  List next;
};

/* a queue is a list and a pointer to the last node */
typedef struct Queue {
  List list;
  List lastNode;
} Queue;

/* We use the functions on lists as defined in 1.3 of the lecture notes.
 */
List newEmptyList();

int isEmptyList (List li);

void listEmptyError();

List addItem(State s, List li);

State firstItem(List li);

List removeFirstNode(List li);

void freeList(List li);

Queue newEmptyQueue();

int isEmptyQueue (Queue q);

void enqueue (State s, Queue *qp);

State dequeue(Queue *qp);

void freeQueue (Queue q);

void insertUnique (State s, Queue *qp);

void printState(State s);

#endif
