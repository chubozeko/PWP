import { ChefsComponent } from './components/chefs/chefs.component';
import { SingleBlogComponent } from './components/single-blog/single-blog.component';
import { WrapperComponent } from './components/wrapper/wrapper.component';
import { AppComponent } from './app.component';
import { AboutComponent } from './components/about/about.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PageNotFoundComponent } from './components/page-not-found/page-not-found.component';

const routes: Routes = [
  { path: '', component: WrapperComponent },
  { path: 'about', component: AboutComponent },
  { path: 'blog', component: SingleBlogComponent },
  { path: 'chefs', component: ChefsComponent },
  { path: '**', component: PageNotFoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
