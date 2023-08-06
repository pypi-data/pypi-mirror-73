class Algo:

    def encode(type,number):
    
        if type==1:
            def base36encode(number):
                if not isinstance(number, (int, int)):
                    raise TypeError('number must be an integer')
                if number < 0:
                    raise ValueError('number must be positive')

                alphabet, base36 = ['0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', '']

                while number:
                    number, i = divmod(number, 36)
                    base36 = alphabet[i] + base36

                return base36 or alphabet[0]

        encoded = base36encode(int(number))
        return encoded

    def decode(type,number):
        if type==1:
            def base36decode(number):
                return int(number, 36)

        decoded = base36decode(number)
        return decoded
            
            
    
