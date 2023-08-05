class cool_funcs:
    
    def __init__(self,data=[],n=10):
        self.data=data
        self.n=n
        pass
        
    def flatten(self):
        """
        This function flattens nested lists
        """
        if self.data:
            def flat(l):
                ans=[]
                for i in l:
                    if type(i)==list:
                        ans.extend(flatten(i))
                    else:
                        ans.append(i)
                return ans
            return flat(self.data)
        else:
            return []
        
    
    def factorize(self,num):
        """
        This returns all prime factors and its power of the number
        """
        def sieveOfEratosthenes(N, s): 
            prime = [False] * (N+1) 
            for i in range(2, N+1, 2): 
                s[i] = 2
            for i in range(3, N+1, 2): 
                if (prime[i] == False): 
                    s[i] = i 
                    for j in range(i, int(N / i) + 1, 2): 
                        if (prime[i*j] == False): 
                            prime[i*j] = True
                            s[i * j] = i 


        def generatePrimeFactors(N): 
            ans=[]
            s = [0] * (N+1) 
            sieveOfEratosthenes(N, s) 
            curr = s[N] 
            cnt = 1
            while (N > 1): 
                N //= s[N]
                if (curr == s[N]): 
                    cnt += 1
                    continue

                ans.append((str(curr),str(cnt))) 

                curr = s[N] 
                cnt = 1
            return ans
        
        return generatePrimeFactors(num)