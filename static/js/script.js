function getimg() {
    var n = {};
    n['address'] = $('#address').val();
    var s = {};
    $('#sublist input').each(function () {
        // console.log($(this).val());
        s[$(this).attr('id')] = $(this).val()
    });
    n['subnet'] = s;
    n = JSON.stringify(n);
    // console.log(n);
    $.ajax({
        type: 'post',
        async: false,
        url: '/compute',
        data: {data: n},
        dataType: 'json',
        success: function (datas) {
            if (datas != 'ERROR') {
                console.log(datas);

                $('#img').empty();
                var a = document.createElement('img');
                a.setAttribute('class', 'img-rounded');
                a.src = datas['a'];
                var b = document.createElement('img');
                b.setAttribute('class', 'img-rounded');
                b.src = datas['b'];

                $('#img').append(a);
                $('#img').append(b);

            }
            else {
                alert('ERROR');
            }
        }
    })
}

function dissublist() {
    $("#sublist").empty();

    if ($('#subnum').val() < 0 || $('#subnum').val() > 64) {
        alert('range: 0-64');
        $('#subnum').val(0);
        return
    }

    for (var i = 0; i < $('#subnum').val(); i++) {
        // var str = '<input class="form-control" id="s{0}" type="text" placeholder="Subnet {1}">'.format(i,i);
        var d = document.createElement('input');
        d.setAttribute('class', 'form-control');
        d.type = 'number';
        d.id = i;
        d.placeholder = 'Subnet  ' + i;

        $("#sublist").append(d);
    }
}

function addnum() {
    $('#subnum').val(Number($('#subnum').val()) + 1);
    dissublist();
}

function delnum() {
    $('#subnum').val(Number($('#subnum').val()) - 1);
    dissublist();
}