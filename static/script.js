// Ortak Arkadaş Bulucu - Frontend JavaScript Kodları
// Bu dosya, web arayüzündeki tüm dinamik işlevleri yönetir

$(document).ready(function() {
  
    function updateUserLists() {
        $.get('/users', function(response) {
            if (response.success) {
                const users = response.users;
                const userOptions = users.map(user => 
                    `<option value="${user}">${user}</option>`
                ).join('');

                // Tüm select elementlerini güncelle
                $('#user1, #user2, #friendUser1, #friendUser2').each(function() {
                    const currentValue = $(this).val();
                    $(this).html('<option value="">Kullanıcı seçin</option>' + userOptions);
                    if (currentValue && users.includes(currentValue)) {
                        $(this).val(currentValue);
                    }
                });
            }
        });
    }

    // Sayfa yüklendiğinde kullanıcı listesini güncelle
    updateUserLists();

  
    $('#addUserForm').on('submit', function(e) {
        e.preventDefault();
        const username = $('#newUsername').val();

        $.ajax({
            url: '/user',
            method: 'POST',
            data: { username: username },
            success: function(response) {
                if (response.success) {
                    alert('Kullanıcı başarıyla eklendi!');
                    $('#newUsername').val(''); 
                    updateUserLists(); 
                } else {
                    alert('Hata: ' + response.error);
                }
            },
            error: function() {
                alert('Bir hata oluştu. Lütfen tekrar deneyin.');
            }
        });
    });

  
    $('#addFriendshipForm').on('submit', function(e) {
        e.preventDefault();
        const user1 = $('#friendUser1').val();
        const user2 = $('#friendUser2').val();

        
        if (user1 === user2) {
            alert('Aynı kullanıcıyı seçemezsiniz!');
            return;
        }

        $.ajax({
            url: '/friendship',
            method: 'POST',
            data: {
                user1: user1,
                user2: user2
            },
            success: function(response) {
                if (response.success) {
                    alert('Arkadaşlık başarıyla eklendi!');
                    $('#friendUser1, #friendUser2').val(''); 
                } else {
                    alert('Hata: ' + response.error);
                }
            },
            error: function() {
                alert('Bir hata oluştu. Lütfen tekrar deneyin.');
            }
        });
    });

  
    $('#friendForm').on('submit', function(e) {
        e.preventDefault();
        
        const user1 = $('#user1').val();
        const user2 = $('#user2').val();

    
        if (user1 === user2) {
            alert('Aynı kullanıcıyı seçemezsiniz!');
            return;
        }

        $('#friendsList').empty();
        $('.error-message').remove();

        $.ajax({
            url: '/find_friends',
            method: 'POST',
            data: {
                user1: user1,
                user2: user2
            },
            success: function(response) {
                if (response.success) {
                    const friends = response.common_friends;
                    
                    if (friends.length > 0) {
                     
                        friends.forEach(friend => {
                            const friendElement = $(`
                                <div class="friend-item">
                                    <img src="https://ui-avatars.com/api/?name=${encodeURIComponent(friend)}&background=random" alt="${friend}">
                                    <span>${friend}</span>
                                </div>
                            `);
                            $('#friendsList').append(friendElement);
                        });
                        $('#result').slideDown(); 
                    } else {
                       
                        $('#result').hide();
                        $('.main-card').append(`
                            <div class="error-message">
                                ${user1} ve ${user2} arasında ortak arkadaş bulunamadı.
                            </div>
                        `);
                    }
                } else {
                    
                    $('.main-card').append(`
                        <div class="error-message">
                            ${response.error}
                        </div>
                    `);
                }
            },
            error: function() {
                
                $('.main-card').append(`
                    <div class="error-message">
                        Bir hata oluştu. Lütfen tekrar deneyin.
                    </div>
                `);
            }
        });
    });
}); 