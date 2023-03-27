const productContainers = [...document.querySelectorAll('.sales-product-container')];
const nxtBtn = [...document.querySelectorAll('.nxt-btn')];
const preBtn = [...document.querySelectorAll('.pre-btn')];

productContainers.forEach((item, i) => {
    let containerDimensions = item.getBoundingClientRect();
    let containerWidth = containerDimensions.width;

    nxtBtn[i].addEventListener('click', () => {
        item.scrollLeft += containerWidth;
    })

    preBtn[i].addEventListener('click', () => {
        item.scrollLeft -= containerWidth;
    })
})




function show(){
    document.getElementById('sidebar').classList.toggle('active');
}


var input = document.querySelector("#phone");
intlTelInput(input, {
    initialCountry: "auto",
    geoIpLookup: function (success, failure) {
        $.get("https://ipinfo.io", function () { }, "jsonp").always(function (resp) {
        var countryCode = (resp && resp.country) ? resp.country : "us";
        success(countryCode);
    });
},
});


function swithTobuyer(){
    // setTimeout(2000);
    document.getElementById('switch-id').addEventListener("change", function(){
        if (this.checked){
            window.location.href = '../pages/buyer.html';   
        }else{
            window.location.href = '../pages/seller.html';   
        }
    });
}
