using System;


class Program {
    static void Main() {
        int w;
        Console.Write("Enter start point : ");
        int n1 = int.Parse(Console.ReadLine());
        Console.Write("Enter end point : ");
        int n2 = int.Parse(Console.ReadLine());
        for (int i = n1; i <= n2; i++) {
            if (i == 1 || i == 0) {
                continue;
            }
            w = 1;
            for (int j = 2; j <= i / 2; j++) {
                if (i % j == 0) {
                    w = 0;
                    break;
                }
            }
            if (w == 1) {
                Console.WriteLine("{0} is prime",i);
            }
        }
        Console.ReadLine();
    }
}