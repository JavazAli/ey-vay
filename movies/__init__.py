def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['remaining_seats'].required = False

    if 'cinema' in self.data:
        try:
            cinema_id = int(self.data.get('cinema'))
            self.fields['showtime'].queryset = ShowTime.objects.filter(cinema_id=cinema_id)
        except (ValueError, TypeError):
            self.fields['showtime'].queryset = ShowTime.objects.none()

    elif self.instance.pk:
        self.fields['showtime'].queryset = ShowTime.objects.filter(
            cinema=self.instance.cinema
        )
    else:
        self.fields['showtime'].queryset = ShowTime.objects.none()