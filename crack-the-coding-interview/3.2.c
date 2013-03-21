/* How would you design a stack which, in addition to push and pop,
   also has a function min which returns the minimum element? Push,
   pop and min should all operate in O(1) time.

   Analyse:
   If i want to save time, i use more space. Using linked list
   implement the stack, then use a seperate pointer to point to the
   minimum element, every push will exa
   Oh, no. I think there is no such way to implement it. Since sort()
   cannot faster than O(nlogn), if i implement this, i will push a
   array to this stack, and use min() to sort it, and i get a O(n)
   sort(). I don't think it will happen.
*/
