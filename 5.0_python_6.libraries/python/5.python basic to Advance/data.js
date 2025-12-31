const studentIds = [];

$('#student-ajax-table tbody tr').each(function () {
    const id = $(this).attr('data-student-id');
    if (id) studentIds.push(id);
});

console.log(studentIds);
