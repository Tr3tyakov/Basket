class BasketEventListener {
    constructor() {
        this.cart = []
        this.totalPrice = 0
        this._init()
    }

    async getCart() {
        try {
            const response = await fetch("http://0.0.0.0:8088/api/products")
            const data = await response.json()
            this.cart = data.cart
            this.totalPrice = data.total_price
            this._updateDisplayPrice();
        } catch (error) {
            console.log("Что-то пошло не так", error)
        }
    }

    _init() {
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('.product').forEach(product => {
                const priceElement = product.querySelector('.price');
                const productName = product.querySelector('h3').innerText;
                const productPrice = parseInt(priceElement.innerText);
                product.addEventListener('click', async () => await this._addToCart(productName, productPrice));
            });
            document.querySelectorAll('.product-category p').forEach((category) => {
                category.addEventListener('click', () => {
                    window.location = category.innerText.toLowerCase() + '.html'; // Перенаправление на соответствующую страницу
                });
            });
        });
    }

    async _addToCart(name, price) {
        try {
            await fetch('http://0.0.0.0:8088/api/create_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({name, price})
            });
            this.cart.push({name, price});
            this.totalPrice += price;
            this._updateDisplayPrice();
        } catch (error) {
            console.error('Что-то пошло не так', error);
        }
    }


    _updateDisplayPrice() {
        const price = document.getElementById('total-price');
        price.innerHTML = `Товаров в корзине: ${this.cart.length}, Общая стоимость: ${this.totalPrice}р.`;
    }

}

export default BasketEventListener; 

