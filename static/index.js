$(document).ready(function () {
    $("button").click(function () {
        const length = parseInt($("#length").val()) || 16;
        const include_specials = $("#specials").is(":checked");
        const include_digits = $("#digits").is(":checked");

        $.ajax({
            url: "http://127.0.0.1:5000/password",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                length: length,
                include_specials: include_specials,
                include_digits: include_digits
            }),
        }).done(function (response) {
            $("#pass").text(response.password);
        });
    })

    // Копирование по клику
    $("#pass").click(function () {
        const text = $(this).text();
        if (text !== "тут пусто") {
            navigator.clipboard.writeText(text).then(() => {
                alert("Пароль скопирован!");
            });
        }
    })
})
