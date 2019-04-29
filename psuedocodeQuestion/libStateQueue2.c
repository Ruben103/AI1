/* LibStateQueue.c, February 2019 */

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "libStateQueue.h"

/* We use the functions on lists as defined in 1.3 of the lecture notes.
 */

List newEmptyList() {
  return NULL;
}

int isEmptyList (List li) {
  return ( li==NULL );
}

void listEmptyError() {
  printf("list empty\n");
  abort();
}

List addItem(State s, List li) {
  List newList = malloc(sizeof(struct ListNode));
  assert(newList!=NULL);
  newList->item = s;
  newList->next = li;
  return newList;
}

State firstItem(List li) {
  if ( li == NULL ) {
    listEmptyError();
  }
  return li->item;
}

List removeFirstNode(List li) {
  List returnList;
  if ( li == NULL ) {
    listEmptyError();
  }
  returnList = li->next;
  free(li);
  return returnList;
}

void freeList(List li) {
  List li1;
  while ( li != NULL ) {
    li1 = li->next;
    free(li);
    li = li1;
  }
  return;
}

/* We define some functions on queues, based on the definitions in 1.3.1 of the
 * lecture notes. Integers are replaced by states, and enqueue has output type void here.
 */

Queue newEmptyQueue () {
  Queue q;
  q.list = newEmptyList();
  q.lastNode = NULL;
  return q;
}

int isEmptyQueue (Queue q) {
  return isEmptyList(q.list);
}

void queueEmptyError () {
  printf("queue empty\n");
  exit(0);
}

void enqueue (State s, Queue *qp) {
  if ( isEmptyList(qp->list) ) {
    qp->list = addItem(s,NULL);
    qp->lastNode = qp->list;
  } else {
    qp->lastNode->next = addItem(s,NULL);
    qp->lastNode = qp->lastNode->next;
  }
}

State dequeue(Queue *qp) {
  State s;
  if ( isEmptyQueue(*qp) ) {
    queueEmptyError();
  }
  s = firstItem(qp->list);
  qp->list = removeFirstNode(qp->list);
  if ( isEmptyList(qp->list) )  {
    qp->lastNode = NULL;
  }
  return s;
}

void freeQueue (Queue q) {
  freeList(q.list);
}

// inserts a state between two others
void insertBetween(List a, List b, State s) {
  a->next = addItem(s, b);
}

// FIFO (BFS) 
void insertUnique (State s, Queue *qp) {
  if ( isEmptyList(qp->list) ) {
    qp->list = addItem(s,NULL);
    qp->lastNode = qp->list;
    return;
  }
  List previous_node = NULL, current_node = qp->list;
  while (current_node != NULL) {
    previous_node = current_node;
    current_node = current_node->next;
  }
  if (current_node == NULL) {
    insertBetween(previous_node, NULL, s);
  }
}

// LIFO (DFS)
//void insertUnique (State s, Queue *qp) {
//  if ( isEmptyList(qp->list) ) {
//    qp->list = addItem(s,NULL);
//    qp->lastNode = qp->list;
//    return;
//  }
//  List previous_node = NULL, current_node = qp->list;
//  if (previous_node == NULL) {
//    qp->list = addItem(s, qp->list);
//  } else {
//    insertBetween(previous_node, current_node, s);
//  }
//  if (current_node == NULL) {
//    insertBetween(previous_node, NULL, s);
//  }
//}

