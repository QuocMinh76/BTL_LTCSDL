function addToCart(id, name, price) {
    event.preventDefault()
    // tra ra doi tuong promise
    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)

        let counter = document.getElementById('cartCounter')
        counter.innerText = data.total_quantity
    }).catch(function(err) {
        console.info(err)
    })
}

function pay() {
    if(confirm('Bạn chắn chắn muốn thanh toán không?') == true) {
        fetch('/api/pay', {
            method: 'post' //Neu quen roi co the viet trong then() nhu the nay luon
        }).then(res => res.json()).then(data => {
            if (data.code == 200)
                location.reload()
        }).catch(err => console.info(err))
    }
}