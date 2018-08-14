import { Component, OnInit } from '@angular/core';

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from "@angular/router";


declare const $: any;


@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {

  constructor(
    private http: HttpClient,
    private router: Router
  ) { }

  posts: any;
  content = '';
  comment = '';

  ngOnInit() {
    if(window.localStorage.getItem('token') == null) {
      this.router.navigate(['/login']);
    }
    this.read_post()
  }

  get_options() {
    let httpOptions = {
      headers: new HttpHeaders({
        'x-access-token': window.localStorage.getItem('token')
      })
    };
    return httpOptions
  }

  read_post() {
    this.http.get(
      'http://10.16.129.116:3000/api/posts/timeline/0',
      this.get_options()
    ).subscribe((data) => {
      if (data['success']) {
        this.posts = data['data'].reverse();
      }
    });
  }

  create_post() {
    let headers = {
      content: this.content,
      openRange: 2
    }
    this.http.post(
      'http://10.16.129.116:3000/api/posts/',
      headers,
      this.get_options()
    ).subscribe((data) => {
      if(data['success']) {
        this.content = ''
        this.read_post()
      }
    });
  }

  beautify_score(score) {
    return (score*100+'').slice(0, 4)
  }

  logout() {
    window.localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }

  set_background(score, a) {
    let code = {
      background:
      'rgba('+(231+(26-231)*score)+', '
      +(202+(188-202)*score)+', '
      +(51+(156-51)*(score))+', '+a+')'
    }
    return code
  }

  create_comment(id) {
    let input_tag = $('[data-comment-post-id='+id+']');
    let headers = {
      content: input_tag.val()
    }
    this.http.post(
      'http://10.16.129.116:3000/api/posts/comment/'+id,
      headers,
      this.get_options()
    ).subscribe((data) => {
      if(data['success']) {
        this.content = ''
        this.read_post()
      }
    });
  }

  delete_post(id) {
    this.http.delete(
      'http://10.16.129.116:3000/api/posts/'+id,
      this.get_options()
    ).subscribe((data) => {
      if(data['success']) {
        this.content = ''
        this.read_post()
      }
    });
  }

}
