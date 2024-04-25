$(document).ready(function() {
    $('#add-student-form').submit(function(e) {
        e.preventDefault();
        var name = $('#name').val();
        $.post('/addStudent', {name: name}, function(data) {
            alert(data);
        });
    });

    $('#delete-student-form').submit(function(e) {
        e.preventDefault();
        var id = $('#id').val();
        $.post('/deleteStudent', {id: id}, function(data) {
            alert(data);
        });
    });

    $('#get-students-button').click(function() {
        $.get('/getStudents', function(data) {
            $('#students').html(data);
        });
    });
});
