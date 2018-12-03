
var checknum = [];
var otable = $('#example').DataTable( {
    "ajax": {
        'url' :  '../index/ajaxTable',
        'data' :  {
                staff : 0
            }
    },
    "columns": [
        { "data": null, render: function ( data, type, row ) {
                 var checkbutton = "<input type='checkbox' style='transform: scale(1.5);width: 30px' id='"+  data.id +"' onclick='checkbutton(this,"+ ( data.id) +")'/>";
                 return checkbutton + ' ' + data.username;
            } },
        { data: null, render: function ( data, type, row ) {
            return data.first_name + ' ' + data.last_name;
        } },
        { "data": "email" },
        { data: null, render: function ( data, type, row ) {
                var status ='';
                if (data.is_active){
                    status = "<a class='btn btn-block' style='padding: 0px' onclick='UserStatus("+ data.id + "," + data.is_active+")'>" +
                   "<img src='../../static/images/check/check.png' style='width: 25px'>" + "</a>";
                }else {
                    status = "<a class='btn btn-block' style='padding: 0px' onclick='UserStatus("+ data.id + "," + data.is_active+")'>" +
                   "<img src='../../static/images/check/uncheck.png' style='width: 20px'>" + "</a>";
                }
                return status;
            } }
        ],
        "language": {
            "lengthMenu": " _MENU_  ",
            "zeroRecords": "Nothing found - sorry",
            "info": "Showing page _PAGE_ of _PAGES_",
            "infoEmpty": "No records available",
            "search":         "",
            "searchPlaceholder": "Search...",
            "infoFiltered": "(filtered from _MAX_ total records)"
        },
        "sDom": '<"pull-left"l><"pull-left"f>tip',
        "sPaginationType": "full_numbers"
    } );

function UserStatus(id, status){
    $.ajax({
            url: "../index/status",
            // csrfmiddlewaretoken: '{{ csrf_token }}'
            data: {
                    userStatus : status,
                    userid: id,
            },
            success: function (result) {
                otable.ajax.reload();
            }
        });
}
$('#example tbody').on( 'click', 'tr', function () {

        $("#example tr").css({'background-color':''});
        $("#example tr td").css({'background-color':''});
        $(this).css({'background-color': '#cccccc'});
        $(this).find('td').eq(0).css({'background-color': '#cccccc'});

        var row = otable.row(this).data();

        var rowEdit = "<a href='../../admin/customer/" + row.id + "' type='button' class='btn' style='-webkit-appearance: none;cursor:pointer;color: green;background-color: white;border: 2px solid green;width:90px;border-radius: 5px'>Edit</a>";

        document.getElementById("userEdit").innerHTML = rowEdit;
    });
    
toastr.options = {
  "closeButton": true,
  "debug": false,
  "positionClass": "toast-top-right",
  "onclick": null,
  "showDuration": "1000",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
};

function checkbutton( checkbox, id){
     if (checkbox.checked)
        {
            checknum.push(id);
        }else {
            checknum.pop(id);
     }
}

function UserDelete() {

    $('#basic').modal('hide');
    if(checknum.length != 0) {
        $.ajax({
            url: "../index/userDel",
            data: {
                data: checknum
            },
            success: function (result) {
                toastr["success"]("Successfully deleted", "Notifications");
                otable.ajax.reload();
            }
        });
    }
}

$('#modal').on('click',function () {
    if (checknum.length != 0) {
        $('#basic').modal('show');
    }
});


