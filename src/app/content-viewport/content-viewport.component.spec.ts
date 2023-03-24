import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContentViewportComponent } from './content-viewport.component';

describe('ContentViewportComponent', () => {
  let component: ContentViewportComponent;
  let fixture: ComponentFixture<ContentViewportComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ContentViewportComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContentViewportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
