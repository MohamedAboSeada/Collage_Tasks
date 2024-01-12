using System;

// [1] take the factors of number 
class Program {
    static void Main() {
        Console.WriteLine("--------------------------");
        Console.WriteLine("| Get Perfect into range |");
        Console.WriteLine("--------------------------\n");
        Console.Write("Enter start point : ");
        int n1 = int.Parse(Console.ReadLine());
        Console.Write("Enter end point : ");
        
        int n2 = int.Parse(Console.ReadLine());
        for (int i = n1; i <= n2; i++) {
            int sum = 0;
            for (int j = 1; j < i; j++) {
                if (i%j == 0) {
                    sum += j;
                }
            }
            if (sum == i) {
                Console.WriteLine("'{0}' is Perfect",i);
            }
        }
        Console.ReadLine();
    }
}