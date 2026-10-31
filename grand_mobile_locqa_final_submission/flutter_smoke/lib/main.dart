import 'package:flutter/material.dart';
import 'l10n/generated/app_localizations.dart';

void main() => runApp(const LocalizationSmokeApp());

class LocalizationSmokeApp extends StatelessWidget {
  const LocalizationSmokeApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
    locale: const Locale('kk'),
    localizationsDelegates: AppLocalizations.localizationsDelegates,
    supportedLocales: AppLocalizations.supportedLocales,
    home: Builder(builder: (context) => Scaffold(
      body: Center(child: Text(AppLocalizations.of(context).predictionsBetsTitle)),
    )),
  );
}
