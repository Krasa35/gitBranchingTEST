#include <stdio.h>
int main()
{
    double a, b, product;
    printf("Enter two numbers: ");
    scanf("%lf %lf", &a, &b);

    // Calculating product
    product = a * a;
    product = product+1;
    product++;

    // %.2lf displays number up to 2 decimal point
    printf("Product = %.2lf", product);
    printf("cos");
    return 0;
}