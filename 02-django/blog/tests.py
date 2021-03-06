from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_test1 = User.objects.create_user(username="TEST1", password="password1")
        self.user_test2 = User.objects.create_user(username="TEST2", password="password2")

        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.post_001 = Post.objects.create(
            title='first post',
            content='Hello World',
            category=self.category_programming,
            author=self.user_test1
        )
        self.post_002 = Post.objects.create(
            title='Second post',
            content='Hello World',
            category=self.category_music,
            author=self.user_test2
        )
        self.post_003 = Post.objects.create(
            title='Third post',
            content='No category',
            author=self.user_test1
        )

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        home_bnt = navbar.find('a', text='Home')
        self.assertEqual(home_bnt.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def test_post_list(self):

        # 포스트 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main_area')
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.category, post_003_card.text)

        self.assertIn(self.user_test1.username.upper(), main_area.text)
        self.assertIn(self.user_test2.username.upper(), main_area.text)

        #포스트가 없는 경우
        Post.object.all.delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main_area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        # 1.1 포스트가 하나 있다.
        post_001 = Post.objects.create(
            title='첫 번째 포스트 입니다.',
            content='첫 번째 포스트의 상세 내용입니다.',
            author=self.user_test1,
        )
        # 1.2 그 포스트의 url은 '/blog/1/'이다
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1 첫 번째 포스트의 url로 접근하면 정상적으로 작동한다(code 200)
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2 포스트 목록 페이지와 같은 네비게이션 바가 있다

        self.navbar_test(soup)
        self.category_card_test(soup)

        # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 있다
        self.assertIn(self.post_001.title, soup.title.text)

        # 2.4 첫 번째 포스트의 제목이 포스트 영역에 있다
        main_area = soup.find('div', id='main_area')
        post_area = main_area.find('div', id='post_area')
        self.assertIn(self.post_001.title, post_area.text) # post_area.title -> 오타 같음

        # 2.5 첫 번째 포스트의 작성자가 포스트 영역에 있다(미구현)
        # 2.6 첫 번째 포스트의 내용이 포스트 영역에 있다.
        self.assertIn(post_001.content, post_area.text)
