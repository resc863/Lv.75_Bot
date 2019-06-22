#include <stdio.h>

int input(char a[100],int b, char c[50]) {
    printf("======================\n");
    printf("이름 : %s\n",a);
    printf("번호 : %d\n",b);
    printf("성별 : %s\n",c);
    printf("======================\n");
}

int main() {
    char name[100];
    int num;
    char sex[50];

    do {
        printf("이름을 입력하세요...\n");
        scanf("%s",&name);

        printf("번호를 입력하세요...\n");
        scanf("%d",&num);

        printf("성별을 입력하세요...\n");
        scanf("%s",&sex);

        input(name,num,sex);

    } while (1);

    return 0;
}
