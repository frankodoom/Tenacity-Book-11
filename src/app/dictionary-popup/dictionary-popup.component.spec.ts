import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DictionaryPopupComponent } from './dictionary-popup.component';

describe('DictionaryPopupComponent', () => {
  let component: DictionaryPopupComponent;
  let fixture: ComponentFixture<DictionaryPopupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DictionaryPopupComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DictionaryPopupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
