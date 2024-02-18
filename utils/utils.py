
def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')

def qtd_total_carrinho(carrinho: dict):
    return sum([item['quantidade'] for item in carrinho.values()])


def preco_total(carrinho:dict):
    
    cart = carrinho.values()
    #total = None
    #for item in cart:
        
    #    if item['preco_quantitativo_promocional']:
    #        total += item['preco_quantitativo_promocional']
    #    
    #    else:  
    #        total += item['preco_quantitativo'] 
         
     
    return sum(
            [
                item['preco_quantitativo_promocional']
                if item['preco_quantitativo_promocional']
                else item['preco_quantitativo']
                for item in cart   
            ]
        )
    
      
        