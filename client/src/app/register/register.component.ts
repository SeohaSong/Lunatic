import { Component, OnInit } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { Router } from "@angular/router";


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  constructor(
    private http: HttpClient,
    private router: Router
  ) { }

  user_id: string;;
  user_pw: string;;
  user_pw_confirm: string;;
  user_name: string;;
  user_mail: string;;

  ngOnInit() {
    if(window.localStorage.getItem('token')) {
      this.router.navigate(['main']);
    }
  }

  create_user() {
    let user = {
      uid: this.user_id,
      password: this.user_pw,
      passwordConfirmation: this.user_pw_confirm,
      name: this.user_name,
      email: this.user_mail
    }
    this.http.post(
      'http://10.16.129.116:3000/api/users', user
    ).subscribe((data) => {
      setTimeout(() => {
        this.request_login()
      }, 1000)
    });
  }

  request_login() {
    let user = {uid: this.user_id, password: this.user_pw}
    this.http.post(
      'http://10.16.129.116:3000/api/auth/login', user
    ).subscribe((data) => {
      if(data['success']) {
        window.localStorage.setItem('token', data['data']);
        this.router.navigate(['main']);
      }
    });
  }

}
