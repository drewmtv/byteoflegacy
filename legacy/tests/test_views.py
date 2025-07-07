import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from legacy.models import Slot

@pytest.mark.django_db
def test_slot_chunk_view_valid(client, mocker):
    url = reverse('legacy:slot_chunk')

    # Mock the helper to return test data
    mock_slots = [
        {
            'slot_number': 1,
            'claimed': True,
            'price': 100,
            'verified': True,
            'name': 'Alice',
            'icon': 'icon_url',
            'front_bg_color': '#fff',
            'front_text_color': '#000',
            'message': 'Hello',
            'link': 'http://example.com',
            'back_bg_color': '#eee',
            'back_text_color': '#111',
        },
        {
            'slot_number': 2,
            'claimed': False,
            'price': 200,
            'verified': False,
            'name': 'Bob',
            'icon': 'icon_url2',
            'front_bg_color': '#ccc',
            'front_text_color': '#222',
            'message': 'World',
            'link': 'http://example.org',
            'back_bg_color': '#ddd',
            'back_text_color': '#333',
        },
    ]

    mocker.patch('legacy.views.get_all_slots_with_status', return_value=mock_slots)

    response = client.get(url, {'offset': 0, 'limit': 2})

    assert response.status_code == 200
    json_data = response.json()
    assert 'slots' in json_data
    assert len(json_data['slots']) == 2
    assert json_data['slots'][0]['slot_number'] == 1

@pytest.mark.django_db
def test_claim_byte_get(client, mocker):
    url = reverse('legacy:claim')

    mocker.patch('legacy.views.get_all_slots_with_status', return_value=[])

    response = client.get(url)

    assert response.status_code == 200
    assert b'<form' in response.content  # Basic check that form is rendered

@pytest.mark.django_db
def test_claim_byte_post_success(client, mocker):
    url = reverse('legacy:claim')

    # Mock upload and validation
    mocker.patch('legacy.views.upload_to_supabase_media', side_effect=lambda f, p: f'https://fake.supabase/{p}')
    mocker.patch('legacy.views.upload_to_supabase_confidential', side_effect=lambda f, p: f'https://fake.supabase/{p}')
    mocker.patch('legacy.views.validate_image_file', return_value=None)

    icon_file = SimpleUploadedFile("icon.png", b"fake-image-content", content_type="image/png")
    proof_file = SimpleUploadedFile("proof.png", b"fake-image-content", content_type="image/png")

    data = {
        'slot_number': 10,
        'name': 'Test User',
        'email': 'testuser@example.com',
        'payment_amount': '100',
        'message': 'Hello world',
        # The form expects string URLs here because of CharField HiddenInput
        'icon': 'some_dummy_icon_url',
        'payment_proof': 'some_dummy_proof_url',
        'front_bg_color': '#ffffff',
        'front_text_color': '#000000',
        'link': '',
        'back_bg_color': '#ffffff',
        'back_text_color': '#000000',
    }

    files = {
        'icon': icon_file,
        'payment_proof': proof_file,
    }

    response = client.post(url, data=data, files=files, follow=True)

    assert response.status_code == 200
    assert 'Claim Submitted!' in response.content.decode()



@pytest.mark.django_db
def test_claim_byte_post_slot_taken(client, mocker):
    url = reverse('legacy:claim')

    # Create a Slot that already exists
    Slot.objects.create(
        slot_number=1,
        name='Taken User',
        email='taken@example.com',
        payment_amount=100,
        message='Taken slot',
        icon='icon_url',
        payment_proof='proof_url',
        verified=True,
    )

    mocker.patch('legacy.views.get_all_slots_with_status', return_value=[])

    icon_file = SimpleUploadedFile("icon.png", b"fake-image-content", content_type="image/png")
    proof_file = SimpleUploadedFile("proof.png", b"fake-image-content", content_type="image/png")

    data = {
        'slot_number': 1,
        'name': 'New User',
        'email': 'newuser@example.com',
        'payment_amount': '150',
        'message': 'Trying to take taken slot',
    }

    files = {
        'icon': icon_file,
        'payment_proof': proof_file,
    }

    response = client.post(url, data=data, files=files, follow=True)

    assert response.status_code == 200
    assert b"already taken or pending" in response.content

@pytest.mark.django_db
def test_claim_success_view(client):
    url = reverse('legacy:success')
    response = client.get(url)

    assert response.status_code == 200
    assert b'Claim Submitted!' in response.content
