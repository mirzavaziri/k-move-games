// Part of the computations for "Games with k moves per turn" (Mirzavaziri, Yaqubi).
// Usage: ./nim4_rows A B out.txt   (rows 0..A, levels 0..B); compile: gcc -O2 -o nim4_rows nim4_rows.c
// Spread-restricted solver for two-move Nim on 4 heaps, rows a<=A, levels b<=B.
// Stores P[a][b][e][f] for positions (a,b,b+e,b+e+f), e+f<=a+3 (boundary layer included).
// Assumes (and verifies at every level) that boundary positions e+f=a+3 are N.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int A,B,W,E;
unsigned char *P;
#define IX(a,b,e,f) ((((size_t)(a)*(B+1)+(b))*E+(e))*E+(f))
static int isP_sorted(int x0,int x1,int x2,int x3){ // sorted
  if(x0+x1+x2+x3==0) return 1;
  if(x0>A) return 0;
  int e=x2-x1,f=x3-x2;
  if(e+f>x0+3) return 0;           // beyond boundary: N by spread lemma (verified inductively)
  if(x1>B) return 0;
  return P[IX(x0,x1,e,f)];
}
static int isP4(int*u){ int t[4]={u[0],u[1],u[2],u[3]};
  for(int i=1;i<4;i++){int k=t[i],j=i-1;while(j>=0&&t[j]>k){t[j+1]=t[j];j--;}t[j+1]=k;}
  return isP_sorted(t[0],t[1],t[2],t[3]); }
int main(int argc,char**argv){
  A=atoi(argv[1]); B=atoi(argv[2]); W=A+2; E=A+4;
  P=calloc((size_t)(A+1)*(B+1)*E*E,1);
  long viol=0;
  for(int b=0;b<=B;b++){
    for(int a=0;a<=A && a<=b;a++){
      for(int s=0;s<=a+3;s++) for(int e=0;e<=s;e++){ int f=s-e;   // process by increasing e+f
        int v[4]={a,b,b+e,b+e+f};
        if(v[0]+v[1]+v[2]+v[3]==0) continue;
        int ne=(v[0]>0)+(v[1]>0)+(v[2]>0)+(v[3]>0);
        int win=(ne<=2);
        int lo=b-W-2; if(lo<0) lo=0;
        for(int i=0;i<4&&!win;i++)for(int j=i+1;j<4&&!win;j++){
          // candidate new values for coord i and j
          for(int xi=v[i]; xi>=0 && !win; xi--){
            if(xi>A && xi<lo) { xi=A+1; continue; }
            for(int xj=v[j]; xj>=0 && !win; xj--){
              if(xj>A && xj<lo) { xj=A+1; continue; }
              int dec=(v[i]-xi)+(v[j]-xj); if(dec<2) continue;
              int u[4]={v[0],v[1],v[2],v[3]}; u[i]=xi; u[j]=xj;
              if(isP4(u)) win=1;
            }
          }
        }
        if(!win){ P[IX(a,b,e,f)]=1; if(e+f==a+3){viol++; fprintf(stderr,"BOUNDARY P: %d %d %d %d\n",v[0],v[1],v[2],v[3]);} }
      }
    }
  }
  printf("boundary violations: %ld\n",viol);
  FILE*o=fopen(argv[3],"w");
  for(int b=0;b<=B;b++)for(int a=0;a<=A&&a<=b;a++)for(int e=0;e<E;e++)for(int f=0;e+f<=a+3&&f<E;f++)
    if(P[IX(a,b,e,f)]) fprintf(o,"%d %d %d %d\n",a,b,b+e,b+e+f);
  fclose(o); return 0;
}
