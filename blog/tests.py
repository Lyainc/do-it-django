from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_alpha = User.objects.create_user(username='alpha', password='alpha1')
        self.user_beta = User.objects.create_user(username='beta', password='beta1')
        
        self.category_people = Category.objects.create(name='people', slug='people')
        self.category_culture = Category.objects.create(name='culture', slug='culture')
        
        self.post_001 = Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = '첫 번째 콘텐츠의 콘텐츠입니다.',
            author = self.user_alpha,
            category = self.category_people,
        )
        self.post_002 = Post.objects.create(
            title = '두 번째 포스트입니다.',
            content = '두 번째 콘텐츠의 콘텐츠입니다.',
            author = self.user_beta,
            category = self.category_culture,
        )
        
        def category_card_test(self, soup):
            categories_card = soup.find('div', id='categories-card')
            self.assertIn('Categories', categories_card.text)
            self.assertIn(f'{self.category_people.name} ({self.category_people.post_set.count()})', categories_card.text)
            self.assertIn(f'{self.category_culture.name} ({self.category_culture.post_set.count()})', categories_card.text)
                    
        def test_post_list(self):
            self.assertEqual(Post.objects.count(), 2)
            
            response = self.client.get('/blog/')
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            self.navbar_test(soup)
            self.category_card_test(soup)
            
            main_area = soup.find('div', id=main_area)
            self.assertNotIn('아직 게시물이 없습니다', main_area.text)
            
            post_001_card = main_area.find('div', id='post-1')
            self.assertIn(self.post_001.title, post_001_card.text)
            self.assertIn(self.post_001.category.name, post_001_card.text)
            
            post_002_card = main_area.find('div', id='post-2')
            self.assertIn(self.post_002.title, post_002_card.text)
            self.assertIn(self.post_002.category.name, post_002_card.text)
            
            self.assertIn(self.user_alpha.username, main_area.text)
            self.assertIn(self.user_beta.username, main_area.text)
            
            # 포스트가 없는 경우
            Post.objects.all.delete()
            self.assertEqual(Post.objects.count(), 0)
            
            response = self.clinet.get('/blog/')
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.content, 'html.parser')
                    
            main_area = soup.find('div', id=main_area)
            self.assertIn('아직 게시물이 없습니다', main_area.text)
        
    def test_post_detail(self):
        
        # 1.2 포스트의 URL은 '/blog/1/'이다.
        self.assertEqual(self.post_001.get_absolute_url(), "/blog/1/")
        
        # 2.1 첫번째 포스트의 URL로 접근하면 정상적으로 작동한다
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 2.2 포스트 목록 페이지와 같은 네비게이션 바가 있다.
        self.navbar_test(soup)
        
        # 2.3 첫번째 포스트의 제목이 웹브라우저 탭 타이틀에 있다.
        self.assertIn(self.post_001.title, soup.title.text)
        
        # 2.4 첫번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('article', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
                
        # 2.5 첫번째 포스트의 작성자(Author)가 있다.
        self.assertIn(self.post_001.author.username, post_area.text)
    
        # 2.6 첫번째 포스트의 내용(Content)가 있다.
        self.assertIn(self.post_001.content, post_area.text)
        
    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)
    
        logo_btn = navbar.find('a', text="Blog Test Page")
        self.assertEqual(logo_btn.attrs['href'], '/')
        
        home_btn = navbar.find('a', text="Home")
        self.assertEqual(home_btn.attrs['href'], '/')
        
        blog_btn = navbar.find('a', text="Blog")
        self.assertEqual(blog_btn.attrs['href'], '/blog/')        
        
        about_me_btn = navbar.find('a', text="About Me")
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')