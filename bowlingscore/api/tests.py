from django.urls import reverse
import json
from django.test import TestCase, Client
from .models import BowlingScore, Player
from .serializers import ScoreSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Player, BowlingScore
from .serializers import PlayerSerializer, ScoreSerializer
from rest_framework.test import APIClient, APITestCase
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class ScoreTests(APITestCase):
    def test_create_player(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('players-list')
        data = {
            'name': 'Barbara',
            'game': 1
            }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(Player.objects.get().name, 'Barbara')


    def test_create_score(self):

        url = reverse('bowling-list')
        player_1 = Player.objects.create(name='Bernice', game=2) 
        data = {
            'player': player_1,
            'frame_1': 1,
            'first_roll': 2,
            'second_roll': 3
            }

        response = self.client.post(url, data.toJSON(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BowlingScore.objects.count(), 1)
        self.assertEqual(BowlingScore.objects.get().frame_score, 5)



# GET All 
class GetAllScoresTest(TestCase):
    """ Test module for GET all Scores API """

    def setUp(self):
        Player.objects.create(name='Bernice', game='4')
        player_1 = Player.objects.get(name='Bernice') 
        BowlingScore.objects.create(
            frame_num=1, player=player_1, first_roll = 10, second_roll=0, tenth_frame_bonus_pins = 0)
        BowlingScore.objects.create(
            frame_num=2, player=player_1, first_roll = 0, second_roll=10, tenth_frame_bonus_pins = 0)
        self.score_3 = {
            'frame_num': 3,
            'player': player_1,  
            'first_roll': 10,
            'second_roll': 0
        }


    def test_get_all_scores(self):
        # get API response
        client = APIClient()
        response = client.get(reverse('bowling-list'))
        # get data from db
        scores = BowlingScore.objects.all()
        serializer = ScoreSerializer(scores, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_score(self):
        client=APIClient()
        response = self.client.get(reverse('bowling-list'), data=json.dumps())
        scores = BowlingScore.objects.get(frame_num=3)
        serializer = ScoreSerializer(scores)
        # self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#GET SINGLE Test
class GetScoreTest(TestCase):
    """ Test module for GET single score API """
    client = APIClient()
    def setUp(self):
        self.harold = Player.objects.create(
            name='Harold', game=2)
        self.ricky = Player.objects.create(
            name='Ricky', game =3)
        self.score_1 = BowlingScore.objects.create(
             frame_num=1, player=self.ricky, first_roll = 10, second_roll=0, tenth_frame_bonus_pins = 0)
        self.score_2 = BowlingScore.objects.create(
            frame_num=1, player=self.harold, first_roll=1, second_roll=2, tenth_frame_bonus_pins = 0)
        

    def test_get_valid_single_player(self):
        response = self.client.get(
            reverse('players-list'), data=json)
        player = Player.objects.get(id=self.harold.id)
        serializer = PlayerSerializer(player)
        self.assertEqual(response, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_player(self):
        response = self.client.get(
            reverse('players-list'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# #POST Test
class CreateNewScoreTest(TestCase):
    """ Test module for inserting a new score record """
    
    def setUp(self):
        self.valid_payload = {"id":1,
        "frame_num":1,
        "first_roll":4,
        "second_roll":4,
        "player":1,
        "strike_spare":"neither",
        "tenth_frame_bonus_pins":0,
        "frame_score":8,
        "total_score":8
        }
        self.invalid_payload = {
            'player': '',
            'frame_num': 4,
            'first_roll': 10,
            'second_roll': '',
        }

    def test_create_valid_score(self):
        client = APIClient()
        response = client.post(
            reverse('bowling-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_score(self):
        client = APIClient()
        response = client.post(
            reverse('bowling-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# PUT Test
class UpdateSingleScoreTest(TestCase):
    """ Test module for updating an existing score record """
    client = Client()
    def setUp(self):
        self.score_1 = BowlingScore.objects.create(
             frame_num=1, player=1, first_roll = 10, second_roll=0)
        self.score_2 = BowlingScore.objects.create(
            frame_num=2, player=2, first_roll=1, second_roll=2)
        self.valid_payload = {
            'player': 'Buffy',
            'frame_num': 4,
            'first_roll': 10,
            'secon_roll': 0
        }
        self.invalid_payload = {
            'player': '',
            'frame_num': 4,
            'first_roll': 10,
            'second_roll': '',
        }

    def test_valid_update_score(self):
        response = client.put(
            reverse('api/bowling', kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_score(self):
        response = client.put(
            reverse('api/bowling', kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



# DELETE Test
class DeleteSingleScoreTest(TestCase):
    """ Test module for deleting an existing score record """
    

    def setUp(self):
        self.billy = Player.objects.create(
            name='Billy', game = 2)
        self.score_1 = BowlingScore.objects.create(
            frame_num = 1, player = self.billy, first_roll=10, second_roll = 0)
        

    def test_valid_delete_score(self):
        client = APIClient()
        response = self.client.delete(
            reverse('bowling-details', kwargs={'pk': self.score_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_score(self):
        client = APIClient()
        response = self.client.delete(
            reverse('bowling-details', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)